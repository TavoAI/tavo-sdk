import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */
const sidebars: SidebarsConfig = {
  docs: [
    'intro',
    {
      type: 'category',
      label: 'Getting Started',
      items: [
        'getting-started/installation',
        'getting-started/configuration',
        'getting-started/authentication',
      ],
    },
    {
      type: 'category',
      label: 'Tools & Integrations',
      items: [
        'tools/cli',
        'tools/vscode-plugin',
        'tools/github-action',
      ],
    },
    {
      type: 'category',
      label: 'Framework Examples',
      items: [
        'examples/django',
        'examples/express',
        'examples/flask',
        'examples/spring-boot',
        'examples/react',
        'examples/vue',
        'examples/angular',
        'examples/fastapi',
        'examples/aspnet-core',
      ],
    },
  ],
};

export default sidebars;
