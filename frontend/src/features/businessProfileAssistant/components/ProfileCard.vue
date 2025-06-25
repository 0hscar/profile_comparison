<template>
  <section class="main-section card-modern profile-card-gap" v-if="profile">
    <div class="profile-card-header">
      <h2 class="main-title card-title-modern">Profile</h2>
      <button
        class="profile-cog-btn"
        @click="$emit('edit-profile')"
        aria-label="Edit Profile"
      >
        <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
          <circle
            cx="11"
            cy="11"
            r="10"
            fill="#f5f8fa"
            stroke="#b0b8c1"
            stroke-width="1"
          />
          <path
            d="M11 7.5A3.5 3.5 0 1 1 7.5 11 3.5 3.5 0 0 1 11 7.5m0-1.5a5 5 0 1 0 5 5 5 5 0 0 0-5-5zm0 7.5a2.5 2.5 0 1 1 2.5-2.5A2.5 2.5 0 0 1 11 13.5z"
            fill="#2d8cf0"
          />
          <path
            d="M11 4v2M11 16v2M4 11h2M16 11h2M6.22 6.22l1.42 1.42M14.36 14.36l1.42 1.42M6.22 15.78l1.42-1.42M14.36 7.64l1.42-1.42"
            stroke="#2d8cf0"
            stroke-width="1.2"
            stroke-linecap="round"
          />
        </svg>
      </button>
    </div>
    <div class="sidebar-business-info card-content-modern">
      <div class="info-row">
        <span class="info-label">Name:</span>
        <span class="info-value">{{ profile.name }}</span>
      </div>
      <div class="info-row">
        <span class="info-label">Address:</span>
        <span class="info-value">{{ profile.address }}</span>
      </div>
      <div class="info-row">
        <span class="info-label">Phone:</span>
        <span class="info-value">{{ profile.phone }}</span>
      </div>
      <div class="info-row">
        <span class="info-label">Website:</span>
        <span class="info-value">
          <a :href="profile.website" target="_blank">{{ profile.website }}</a>
        </span>
      </div>
      <div class="info-row">
        <span class="info-label">Category:</span>
        <span class="info-value">{{ profile.category }}</span>
      </div>
      <div class="info-row">
        <span class="info-label">Price Level:</span>
        <span class="info-value">{{ profile.priceLevel }}</span>
      </div>
    </div>
    <div class="profile-health-header">
      <span class="profile-health-score-label">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <circle cx="12" cy="12" r="12" fill="#2d8cf0" fill-opacity="0.12" />
          <path
            d="M7 13.5L10.5 17L17 10.5"
            stroke="#2d8cf0"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
        Health Score
      </span>
      <span class="profile-health-score-value">
        {{ gamification.score }}%
      </span>
    </div>
    <div class="profile-health-bar-outer">
      <div
        class="profile-health-bar-inner"
        :style="{ width: gamification.score + '%' }"
      ></div>
    </div>
    <div v-if="gamification.score === 100" class="score-complete-modern">
      🎉 Your profile is fully optimized! Keep it fresh for ongoing rewards.
    </div>
    <div class="profile-health-stats-row">
      <div class="profile-health-stat">
        <span class="stat-label">Rating</span>
        <span class="stat-value">
          {{ profile.rating }}
          <span v-if="profile.review_count" class="stat-sub">
            ({{ profile.review_count }} reviews)
          </span>
        </span>
      </div>
      <div class="profile-health-stat">
        <span class="stat-label">Recent Reviews</span>
        <span class="stat-value">
          {{ profile.recentReviews }}
          <span class="stat-sub">(last 3 months)</span>
        </span>
      </div>
      <div class="profile-health-stat">
        <span class="stat-label">Photos</span>
        <span class="stat-value">{{ profile.photoCount }}</span>
      </div>
      <div class="profile-health-stat">
        <span class="stat-label">Menu</span>
        <span class="stat-value">
          <a
            v-if="profile.menuAvailable"
            :href="profile.menuUrl"
            target="_blank"
            >View Menu</a
          >
          <span v-else>No menu online</span>
        </span>
      </div>
      <div class="profile-health-stat">
        <span class="stat-label">Completeness</span>
        <span class="stat-value">{{ profile.profileCompleteness }}%</span>
      </div>
      <div class="profile-health-stat">
        <span class="stat-label">Last Update</span>
        <span class="stat-value">{{ profile.lastProfileUpdate }}</span>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  profile: { type: Object, required: true },
  gamification: { type: Object, required: true },
});
</script>

<style scoped>
.profile-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
}

.profile-cog-btn {
  background: none;
  border: none;
  box-shadow: none;
  padding: 0.1em;
  margin: 0;
  cursor: pointer;
  position: absolute;
  top: 0.2em;
  right: 0.2em;
  z-index: 2;
  display: flex;
  align-items: center;
  transition: background 0.2s;
}
.profile-cog-btn:focus {
  outline: 2px solid #2d8cf0;
}
.profile-cog-btn svg {
  display: block;
}

.sidebar-business-info {
  display: flex;
  flex-direction: column;
  gap: 0.7em;
}

.info-row {
  display: flex;
  gap: 0.7em;
  margin-bottom: 0.2em;
}
.info-label {
  color: #888;
  font-size: 0.98em;
  font-weight: 500;
  min-width: 90px;
  display: inline-block;
}
.info-value {
  color: #222;
  font-size: 1.08em;
  font-weight: 600;
  word-break: break-word;
}

.profile-health-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.7em;
}

.profile-health-score-label {
  display: flex;
  align-items: center;
  gap: 0.5em;
  font-weight: 600;
  color: #2d8cf0;
  font-size: 1.1em;
  letter-spacing: 0.01em;
}

.profile-health-score-value {
  font-size: 1.5em;
  font-weight: 700;
  color: #222;
  letter-spacing: -0.01em;
}

.profile-health-bar-outer {
  width: 100%;
  height: 18px;
  background: #e6eaf0;
  border-radius: 9px;
  overflow: hidden;
  margin-bottom: 0.7em;
  box-shadow: 0 1px 4px #2d8cf005;
}

.profile-health-bar-inner {
  height: 100%;
  background: linear-gradient(90deg, #2d8cf0 60%, #5ad1e6 100%);
  border-radius: 9px 0 0 9px;
  transition: width 0.5s cubic-bezier(0.77, 0, 0.18, 1);
}

.score-complete-modern {
  background: #e6f9e6;
  color: #1a7f37;
  border-radius: 8px;
  padding: 0.7em 1em;
  font-size: 1.05em;
  margin-bottom: 0.7em;
  display: flex;
  align-items: center;
  gap: 0.5em;
}

.profile-health-stats-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5em 2.5em;
  margin-top: 0.5em;
}

.profile-health-stat {
  min-width: 140px;
  flex: 1 1 140px;
  display: flex;
  flex-direction: column;
  gap: 0.15em;
  margin-bottom: 0.5em;
}

.stat-label {
  color: #888;
  font-size: 0.98em;
  font-weight: 500;
  margin-bottom: 0.1em;
}

.stat-value {
  color: #222;
  font-size: 1.08em;
  font-weight: 600;
  word-break: break-word;
}

.stat-sub {
  color: #b0b8c1;
  font-size: 0.93em;
  font-weight: 400;
  margin-left: 0.3em;
}
</style>
