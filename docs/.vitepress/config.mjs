import { defineConfig } from 'vitepress'

export default defineConfig({
  title: "RE:now!text Wiki",
  description: "终端无限，故事可见",
  cleanUrls: true,

  themeConfig: {
    logo: 'https://afsweb.qzz.io/logo.svg',

    // 顶部导航栏 (nav)
    nav: [
      { text: '首页', link: '/' },
      { text: '指南', link: '/guide' },
      { text: '关于', link: '/about' }
    ],

    // 侧边栏 (sidebar) - 根据路径显示不同内容
    sidebar: {
      // 当用户在 /guide 路径下时，显示这个侧边栏
      '/guide': [
        {
          text: '入门指南',
          // collapsed: false, // 默认展开
          items: [
            { text: '介绍', link: '/guide' },
            { text: '快速开始', link: '/guide#快速开始' }
          ]
        }
      ]
    },

    // 社交链接
    socialLinks: [
      { icon: 'github', link: 'https://github.com/mifongjvav/RE-now-text' }
    ],

    // 页脚
    footer: {
      message: '基于 MIT 许可发布',
      copyright: 'Copyright © 2026 Argon'
    },

    // 编辑此页链接
    editLink: {
      pattern: 'https://github.com/mifongjvav/RE-now-text/edit/dev/docs/:path',
      text: '在 GitHub 上编辑此页'
    },

    // 上次更新
    lastUpdated: {
      text: '最后更新于',
      formatOptions: {
        dateStyle: 'short',
        timeStyle: 'short'
      }
    }
  }
})