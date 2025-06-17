/* eslint-env node */
module.exports = {
  env: {
    browser: true,
    es2021: true,
  },
  parser: "vue-eslint-parser",
  parserOptions: {
    parser: "@babel/eslint-parser",
    ecmaVersion: 2020,
    sourceType: "module",
  },
  extends: ["eslint:recommended", "plugin:vue/recommended"],
  globals: {
    defineProps: "readonly",
    defineEmits: "readonly",
    defineExpose: "readonly",
    withDefaults: "readonly",
  },
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
