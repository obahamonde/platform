<script setup lang="ts">
const { signinWithPopup, loginWithGithub } = useAuth();
const { query } = useRoute();
const { state } = useStore();
const githubhook = async (code: string) => {
  const res = await loginWithGithub(code);
  const { user, token } = res;
  state.user = user;
  state.token = token;
  state.githubUser = true;
  state.notifications.push({
    message: `Welcome ${state.user!.name}`,
    status: "success",
  });
};

const authCode = computed(() => query?.code?.toString());

const user = computed(() => state.user);

onMounted(async () => {
  if (authCode.value) {
    await githubhook(authCode.value);
  }
});
</script>
<template>
          <section v-if="user" class="container">
            Welcome! {{ user.name }}!
  </section>
  <section v-else class="container">
    <button class="social-login" @click.prevent="signinWithPopup()">
      Login with Github
      <Icon icon="logos:github-icon" class="social-btn" />
    </button>
  </section>
</template>
<route lang="yaml">
meta:
  title: Login
  description: Login
  keywords: Login
  layout: authlayout
</route>
