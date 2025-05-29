<template>
  <button
    :class="['app-btn', variant, { block, round }]"
    :type="type"
    :disabled="disabled"
    @click="$emit('click', $event)"
  >
    <slot />
  </button>
</template>

<script>
export default {
  name: "AppButton",
  props: {
    type: {
      type: String,
      default: "button"
    },
    variant: {
      type: String,
      default: "primary" // options: primary, secondary, danger, etc.
    },
    block: {
      type: Boolean,
      default: false
    },
    round: {
      type: Boolean,
      default: false
    },
    disabled: {
      type: Boolean,
      default: false
    }
  }
};
</script>

<style scoped>
.app-btn {
  display: inline-block;
  font-family: inherit;
  font-size: 1rem;
  padding: 0.7rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.2s, color 0.2s, box-shadow 0.2s;
  background: #2d8cf0;
  color: #fff;
  box-shadow: 0 2px 8px #0001;
  outline: none;
}
.app-btn.primary {
  background: #2d8cf0;
  color: #fff;
}
.app-btn.primary:hover:not(:disabled) {
  background: #1761a0;
}
.app-btn.secondary {
  background: #f5f8fa;
  color: #2d8cf0;
  border: 1px solid #2d8cf0;
}
.app-btn.secondary:hover:not(:disabled) {
  background: #e6f7ff;
}
.app-btn.danger {
  background: #d93025;
  color: #fff;
}
.app-btn.danger:hover:not(:disabled) {
  background: #a61b0b;
}
.app-btn.block {
  display: block;
  width: 100%;
}
.app-btn.round {
  border-radius: 50px;
  padding-left: 2.2rem;
  padding-right: 2.2rem;
}
.app-btn:disabled {
  background: #b3d4fc;
  color: #fff;
  cursor: not-allowed;
  opacity: 0.7;
}
</style>
