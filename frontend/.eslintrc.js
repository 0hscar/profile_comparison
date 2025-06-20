/* eslint-env node */
module.exports = {
  env: {
    browser: true,
    es2021: true,
  },
  parser: "vue-eslint-parser",
  parserOptions: {
    ecmaVersion: 12,
    sourceType: "module",
  },
  extends: ["eslint:recommended", "plugin:vue/vue3-essential"],
  overrides: [
    {
      files: ["*.vue", "*.js", "*.ts", "*.spec.js", "*.test.js"],
      env: {
        jest: true,
      },
      rules: {
        "vue/multi-word-component-names": "off",
      },
    },
  ],
  rules: {},
};
