import numpy as np
import soundfile as sf
import sounddevice as sd
import spaudiopy as sp
from spaudiopy import decoder, utils
import threading
import os
import sys
import time
import audioread

def resource_path(relative_path):
    """获取资源的绝对路径"""
    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = ""

    return os.path.join(base_path, relative_path)


class SpatialAudioPlayer:
    """空间音频播放器，支持暂停、停止、音量调节"""
    
    def __init__(self):
        self.stream = None
        self.audio = None
        self.fs = None
        self.position = 0
        self.is_playing = False
        self.is_paused = False
        self.volume = 1.0
        self.lock = threading.Lock()
    
    def _read_audio(self, audio_file_path):
        """
        读取音频文件，支持 WAV、FLAC、OGG、MP3 等格式
        
        返回:
            audio: numpy 数组 (samples, channels)
            fs: 采样率
        """
        full_path = resource_path(audio_file_path)
        
        # 判断文件扩展名
        ext = os.path.splitext(full_path)[1].lower()
        
        # MP3 格式用 audioread 读取
        if ext == '.mp3':
            with audioread.audio_open(full_path) as f:
                fs = f.samplerate
                channels = f.channels
                _duration = f.duration
                
                # 读取所有音频数据
                audio_data = []
                for buf in f:
                    # audioread 返回的是 bytes，转换为 int16 数组
                    samples = np.frombuffer(buf, dtype=np.int16)
                    audio_data.append(samples)
                
                # 合并所有数据
                audio = np.concatenate(audio_data)
                
                # 重塑为 (samples, channels)
                audio = audio.reshape(-1, channels)
                
                # 归一化到 [-1, 1] (int16 范围是 -32768 到 32767)
                audio = audio.astype(np.float32) / 32768.0
                
                return audio, fs
        
        # 其他格式用 soundfile 读取 (WAV, FLAC, OGG, AIFF 等)
        else:
            audio, fs = sf.read(full_path)
            if len(audio.shape) == 1:
                audio = audio[:, np.newaxis]
            return audio, fs
    
    def load(self, audio_file_path, mode=None, sofa_file_path=None, 
             speaker_layout=None, source_position=None):
        """
        加载并处理音频
        
        参数:
            audio_file_path: 音频文件路径 (支持 WAV, FLAC, OGG, MP3 等)
            mode: None=立体声, 1=HRTF, 2=VBAP
            sofa_file_path: HRTF模式下的sofa文件路径
            speaker_layout: VBAP模式下的扬声器布局 [[az, el], ...]
            source_position: VBAP模式下的声源位置 [az, el]
        """
        # 读取音频（支持 MP3）
        audio, fs = self._read_audio(audio_file_path)
        
        # 根据模式处理音频
        if mode == 1:  # HRTF模式
            if sofa_file_path is None:
                raise ValueError("HRTF模式需要提供 sofa_file_path")
            
            hrtf = sp.IO.load_sofa(sofa_file_path)
            # 标准立体声扬声器布局
            ls_dirs = np.radians([[30, 0], [-30, 0]])
            azi = ls_dirs[:, 0]
            colat = np.pi/2 - ls_dirs[:, 1]
            ls_setup = decoder.LoudspeakerSetup(azi, colat)
            
            # 双耳化
            audio = decoder.binauralize(audio, hrtf, ls_setup, interpolate=True)
        
        elif mode == 2:  # VBAP模式
            if speaker_layout is None or source_position is None:
                raise ValueError("VBAP模式需要提供 speaker_layout 和 source_position")
            
            # 扬声器布局
            ls_dirs = np.radians(speaker_layout)
            azi = ls_dirs[:, 0]
            colat = np.pi/2 - ls_dirs[:, 1]
            ls_setup = decoder.LoudspeakerSetup(azi, colat)
            
            # 声源位置
            src_azi = np.radians(source_position[0])
            src_colat = np.pi/2 - np.radians(source_position[1])
            src_vec = utils.sph2cart(src_azi, src_colat, 1)
            
            # VBAP增益
            gains = decoder.vbap(src_vec[np.newaxis, :], ls_setup).flatten()
            
            # 应用增益
            audio = audio @ np.diag(gains)
        
        # 立体声模式不需要额外处理
        self.audio = audio
        self.fs = fs
        self.position = 0
    
    def callback(self, outdata, frames, _time, status):
        """音频回调函数"""
        
        with self.lock:
            if not self.is_playing:
                outdata.fill(0)
                return
            
            if self.is_paused:
                outdata.fill(0)
                return
            
            start = int(self.position)
            end = int(start + frames)
            
            # 播放结束检测
            if start >= len(self.audio):
                outdata.fill(0)
                self.is_playing = False
                self.position = 0
                raise sd.CallbackStop
            
            if end <= len(self.audio):
                frame_data = self.audio[start:end]
            else:
                frame_data = self.audio[start:]
                if len(frame_data) < frames:
                    pad = np.zeros((frames - len(frame_data), self.audio.shape[1]))
                    frame_data = np.vstack([frame_data, pad])
            
            # 应用音量
            frame_data = frame_data * self.volume
            
            outdata[:] = frame_data
            self.position += frames
    
    def play(self, block=False):
        """开始播放
        
        参数:
            block: 是否阻塞直到播放完成
        """
        if self.audio is None:
            print("请先调用 load() 加载音频")
            return
        
        with self.lock:
            if self.stream is None:
                self.stream = sd.OutputStream(
                    samplerate=self.fs,
                    channels=self.audio.shape[1],
                    callback=self.callback,
                    blocksize=3072
                )
            
            self.is_playing = True
            self.is_paused = False
            
            if not self.stream.active:
                self.stream.start()
        
        # 阻塞等待播放完成
        if block:
            while self.is_playing:
                time.sleep(0.1)
            
            # 播放完成后清理
            with self.lock:
                if self.stream:
                    self.stream.stop()
                    self.stream.close()
                    self.stream = None
    
    def pause(self):
        """暂停播放"""
        with self.lock:
            self.is_paused = True
    
    def resume(self):
        """恢复播放"""
        with self.lock:
            self.is_paused = False
    
    def stop(self):
        """停止播放并重置位置"""
        with self.lock:
            self.is_playing = False
            self.position = 0
            if self.stream:
                self.stream.stop()
    
    def set_volume(self, volume):
        """
        设置音量
        volume: 0.0 ~ 2.0
        """
        with self.lock:
            self.volume = max(0.0, min(2.0, volume))
    
    def seek(self, seconds):
        """
        跳转到指定时间（秒）
        """
        with self.lock:
            self.position = int(seconds * self.fs)
            self.position = max(0, min(self.position, len(self.audio)))
    
    def get_position(self):
        """获取当前播放位置（秒）"""
        with self.lock:
            return self.position / self.fs
    
    def get_duration(self):
        """获取音频总时长（秒）"""
        if self.audio is None:
            return 0
        return len(self.audio) / self.fs