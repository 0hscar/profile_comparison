<template>
  <div
    class="restaurant-card"
    :class="{ user: isUser, expanded: expanded }"
    @click="toggleExpand"
    tabindex="0"
    @keydown.enter.space="toggleExpand"
    :aria-expanded="expanded.toString()"
    role="button"
  >
    <div class="minimized-view">
      <h3>
        {{ card.title || card.name || "Not found" }}
        <span v-if="isUser" class="badge">Your Restaurant</span
        ><br v-if="isUser" />
        <a
          v-if="card.title || card.name"
          class="google-link"
          :href="`https://www.google.com/search?q=${encodeURIComponent(
            card.title || card.name
          )}`"
          target="_blank"
          rel="noopener"
          @click.stop
          >🔎 Google</a
        >
      </h3>
      <div class="min-fields">
        <span
          v-if="card.price_level != null && card.price_level !== ''"
          class="min-field"
        >
          💲{{ card.price_level }}
        </span>
        <span v-if="card.rating !== undefined" class="min-field">
          ⭐ {{ card.rating }}
        </span>
      </div>
      <span class="expand-indicator">{{ expanded ? "▲" : "▼" }}</span>
    </div>
    <transition name="expand">
      <div v-if="expanded" class="expanded-view">
        <div v-if="card.photos && card.photos.length">
          <img :src="card.photos[0]" alt="Photo" class="photo" />
        </div>
        <ul class="fields-list">
          <li v-for="(value, key) in displayFields" :key="key">
            <strong>{{ formatKey(key) }}:</strong>
            <template v-if="key === 'website' && value">
              <a :href="value" target="_blank">{{ value }}</a>
            </template>
            <template v-else-if="key === 'menu_url' && value">
              <a :href="value" target="_blank">View Menu</a>
            </template>
            <template v-else-if="key === 'opening_hours' && value">
              <span v-if="typeof value === 'string'">{{ value }}</span>
              <ul v-else-if="Array.isArray(value)">
                <li v-for="(hour, idx) in value" :key="idx">{{ hour }}</li>
              </ul>
            </template>
            <template v-else-if="Array.isArray(value)">
              {{ value.join(", ") }}
            </template>
            <template v-else-if="typeof value === 'boolean'">
              {{ value ? "Yes" : "No" }}
            </template>
            <template v-else>
              {{
                value !== undefined && value !== null && value !== ""
                  ? value
                  : "Not found"
              }}
            </template>
          </li>
        </ul>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: "RestaurantCard",
  props: {
    card: { type: Object, required: true },
    isUser: { type: Boolean, default: false },
  },
  data() {
    return {
      expanded: false,
    };
  },
  computed: {
    displayFields() {
      // Exclude fields that are shown elsewhere or not useful for display
      const exclude = [
        "title",
        "name",
        "photos",
        "place_id",
        "id",
        "geometry",
        "icon",
        "icon_background_color",
        "icon_mask_base_uri",
      ];
      // Always show these fields first if present, in this order
      const preferredOrder = [
        "address",
        "average_rating",
        "rating",
        "user_ratings_total",
        "review_count",
        "description",
        "menu_url",
        "opening_hours",
        "website",
        "phone_number",
        "price_level",
        "types",
      ];
      const fields = {};
      // Add preferred fields in order
      preferredOrder.forEach((key) => {
        if (this.card[key] !== undefined && !exclude.includes(key)) {
          fields[key] = this.card[key];
        }
      });
      // Add any other fields not already included
      Object.keys(this.card).forEach((key) => {
        if (!Object.hasOwn(fields, key) && !exclude.includes(key)) {
          fields[key] = this.card[key];
        }
      });
      return fields;
    },
  },
  methods: {
    formatKey(key) {
      // Convert snake_case or camelCase to Title Case for display
      return key
        .replace(/_/g, " ")
        .replace(/([a-z])([A-Z])/g, "$1 $2")
        .replace(/\b\w/g, (l) => l.toUpperCase());
    },
    toggleExpand(e) {
      // Only expand/collapse if not clicking a link
      if (e && e.target && (e.target.tagName === "A" || e.target.closest("a")))
        return;
      this.expanded = !this.expanded;
    },
  },
};
</script>

<style scoped>
.restaurant-card {
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1.2rem;
  background: #fff;
  box-shadow: 0 1px 4px #0001;
  position: relative;
  transition: box-shadow 0.2s, background 0.2s;
  word-break: normal;
  overflow-wrap: anywhere;
  white-space: normal;
  cursor: pointer;
  outline: none;
}
.restaurant-card.user {
  border: 2px solid #2d8cf0;
  background: #e6f7ff;
  word-break: normal;
  overflow-wrap: anywhere;
  white-space: normal;
}
.restaurant-card.expanded {
  box-shadow: 0 4px 16px #0002;
  background: #fafdff;
}
.badge {
  background: #2d8cf0;
  color: #fff;
  border-radius: 4px;
  padding: 0.2em 0.6em;
  font-size: 0.8em;
  margin-left: 0.5em;
}
.google-link {
  margin-left: 0.7em;
  font-size: 0.95em;
  color: #1761a0;
  text-decoration: none;
  vertical-align: middle;
  transition: color 0.2s;
}
.google-link:hover {
  color: #2d8cf0;
  text-decoration: underline;
}
.photo {
  width: 100%;
  max-width: 300px;
  border-radius: 4px;
  margin-top: 0.5em;
  box-shadow: 0 1px 4px #0002;
}
ul {
  margin: 0.3em 0 0.3em 1.2em;
  padding: 0;
}
.min-fields {
  margin-top: 0.5em;
  font-size: 1.05em;
  color: #444;
  display: flex;
  gap: 1.2em;
  align-items: center;
}
.min-field {
  display: inline-block;
}
.expand-indicator {
  float: right;
  font-size: 1.2em;
  color: #aaa;
  margin-top: 0.2em;
  margin-right: 0.2em;
  user-select: none;
}
.restaurant-card:focus {
  box-shadow: 0 0 0 2px #2d8cf0;
}
.expand-enter-active,
.expand-leave-active {
  transition: max-height 0.25s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.25s;
}
.expand-enter,
.expand-leave-to {
  max-height: 0;
  opacity: 0;
  overflow: hidden;
}
.expanded-view {
  margin-top: 1em;
}
</style>
