import type * as Preset from '@docusaurus/preset-classic';
import type { Config } from '@docusaurus/types';
import { themes as prismThemes } from 'prism-react-renderer';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Tavo AI SDK',
  tagline: 'Multi-language SDK for AI security and compliance',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://tavoai.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  baseUrl: '/tavo-sdk/',

  // GitHub pages deployment config.
  organizationName: 'TavoAI', // Your GitHub org/user name.
  projectName: 'tavo-sdk', // Your repo name.

  onBrokenLinks: 'throw',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/TavoAI/tavo-sdk/tree/main/docs-site/',
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
          // Useful options to enforce blogging best practices
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Tavo AI SDK',
      logo: {
        alt: 'Tavo AI Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docs',
          position: 'left',
          label: 'Documentation',
        },
        {to: '/blog', label: 'Blog', position: 'left'},
        {
          type: 'dropdown',
          label: 'GitHub',
          position: 'right',
          items: [
            {
              label: 'API Server',
              href: 'https://github.com/TavoAI/api-server',
            },
            {
              label: 'CLI Tool',
              href: 'https://github.com/TavoAI/tavo-cli',
            },
            {
              label: 'VSCode Plugin',
              href: 'https://github.com/TavoAI/vscode-plugin',
            },
            {
              label: 'GitHub Action',
              href: 'https://github.com/TavoAI/tavo-action',
            },
            {
              label: 'Python SDK',
              href: 'https://github.com/TavoAI/tavo-python-sdk',
            },
            {
              label: 'Documentation',
              href: 'https://github.com/TavoAI/tavo-sdk',
            },
          ],
        },
        {
          href: 'https://gettavo.com',
          label: 'Sign Up',
          position: 'right',
        },
        {
          href: 'https://tavoai.net',
          label: 'Dashboard',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Product',
          items: [
            {
              label: 'Sign Up',
              href: 'https://gettavo.com',
            },
            {
              label: 'Dashboard',
              href: 'https://tavoai.net',
            },
            {
              label: 'API Documentation',
              to: '/docs/intro',
            },
          ],
        },
        {
          title: 'Tools',
          items: [
            {
              label: 'CLI Tool',
              href: 'https://github.com/TavoAI/tavo-cli',
            },
            {
              label: 'VSCode Plugin',
              href: 'https://github.com/TavoAI/vscode-plugin',
            },
            {
              label: 'GitHub Action',
              href: 'https://github.com/TavoAI/tavo-action',
            },
          ],
        },
        {
          title: 'Resources',
          items: [
            {
              label: 'Blog',
              to: '/blog',
            },
            {
              label: 'GitHub Organization',
              href: 'https://github.com/TavoAI',
            },
            {
              label: 'Python SDK',
              href: 'https://github.com/TavoAI/tavo-python-sdk',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Tavo AI. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
