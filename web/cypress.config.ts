import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    setupNodeEvents() {
      // implement node event listeners here
    }
  },

  component: {
    devServer: {
      framework: 'next',
      bundler: 'webpack'
    },
    supportFile: 'cypress/support/component.ts',
    specPattern: '**/*.cy.{js,jsx,ts,tsx}',
    // Configure viewport for consistent testing
    viewportWidth: 1280,
    viewportHeight: 720
  },
  screenshotOnRunFailure: false,
  video: false
});
