import { FlatCompat } from '@eslint/eslintrc';
import tanstackPlugin from '@tanstack/eslint-plugin-query';
import eslintConfigPrettier from 'eslint-config-prettier/flat';
import importPlugin from 'eslint-plugin-import';
import simpleImportSort from 'eslint-plugin-simple-import-sort';
import unusedImports from 'eslint-plugin-unused-imports';
import { dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname
});

const eslintConfig = [
  eslintConfigPrettier,
  ...compat.extends('next/core-web-vitals', 'next/typescript'),
  {
    ignores: [
      'node_modules/**',
      '.next/**',
      'out/**',
      'build/**',
      'next-env.d.ts'
    ]
  },
  {
    plugins: {
      import: importPlugin,
      'simple-import-sort': simpleImportSort,
      'unused-imports': unusedImports,
      '@tanstack/query': tanstackPlugin
    },
    rules: {
      // ESLINT
      'no-extra-boolean-cast': 'off',
      // UNUSED IMPORTS
      'unused-imports/no-unused-imports': 'error',
      // IMPORT SORT
      'simple-import-sort/imports': 'error',
      'simple-import-sort/exports': 'error',
      'import/first': 'error',
      'import/newline-after-import': 'error',
      'import/no-duplicates': 'error'
    }
  },
  {
    files: ['**/*.d.ts'],
    rules: {
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/no-unused-vars': 'off'
    }
  },
  {
    files: ['*.js', '*.jsx', '*.ts', '*.tsx'],
    rules: {
      'simple-import-sort/imports': [
        'error',
        {
          groups: [
            // `react` first, `next` second, then packages starting with a character
            [
              '^react',
              '^next',
              '^[a-z]',
              '^@',
              '^components(/.*|$)',
              '^stores(/.*|$)',
              '^utils(/.*|$)',
              '^hooks(/.*|$)',
              '^services(/.*|$)',
              '^\\.\\.(?!/?$)',
              '^\\.\\./?$',
              '^\\./(?=.*/)(?!/?$)',
              '^\\.(?!/?$)',
              '^\\./?$'
            ],
            // Models and types (new Array makes blank space between groups)
            ['^models']
          ]
        }
      ]
    }
  }
];

export default eslintConfig;
