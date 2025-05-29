<template>
  <div class="restaurant-card" :class="{ user: isUser }">
    <h3>
      {{ card.title || card.name || "Not found" }}
      <span v-if="isUser" class="badge">Your Restaurant</span><br v-if="isUser" />
    </h3>
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
          {{ value.join(', ') }}
        </template>
        <template v-else-if="typeof value === 'boolean'">
          {{ value ? "Yes" : "No" }}
        </template>
        <template v-else>
          {{ value !== undefined && value !== null && value !== '' ? value : "Not found" }}
        </template>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "RestaurantCard",
  props: {
    card: { type: Object, required: true },
    isUser: { type: Boolean, default: false }
  },
  computed: {
    displayFields() {
      // Exclude fields that are shown elsewhere or not useful for display
      const exclude = [
        "title", "name", "photos", "place_id", "id", "geometry", "icon", "icon_background_color", "icon_mask_base_uri"
      ];
      // Always show these fields first if present, in this order
      const preferredOrder = [
        "address", "average_rating", "rating", "user_ratings_total", "review_count", "description", "menu_url", "opening_hours", "website", "phone_number", "price_level", "types"
      ];
      const fields = {};
      // Add preferred fields in order
      preferredOrder.forEach(key => {
        if (this.card[key] !== undefined && !exclude.includes(key)) {
          fields[key] = this.card[key];
        }
      });
      // Add any other fields not already included
      Object.keys(this.card).forEach(key => {
        if (!Object.hasOwn(fields, key) && !exclude.includes(key)) {
          fields[key] = this.card[key];
        }
      });
      return fields;
    }
  },
  methods: {
    formatKey(key) {
      // Convert snake_case or camelCase to Title Case for display
      return key
        .replace(/_/g, ' ')
        .replace(/([a-z])([A-Z])/g, '$1 $2')
        .replace(/\b\w/g, l => l.toUpperCase());
    }
  }
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
  transition: box-shadow 0.2s;
  word-break: normal;
  overflow-wrap: anywhere;
  white-space: normal;
}
.restaurant-card.user {
  border: 2px solid #2d8cf0;
  background: #e6f7ff;
  word-break: normal;
  overflow-wrap: anywhere;
  white-space: normal;
}
.badge {
  background: #2d8cf0;
  color: #fff;
  border-radius: 4px;
  padding: 0.2em 0.6em;
  font-size: 0.8em;
  margin-left: 0.5em;
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
</style>
