<script setup lang="ts">
const { loginWithGithub, signinWithPopup } = useAuth();
const { query } = useRoute();

const authCode = computed(() => query?.code?.toString());

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
onMounted(async () => {
  if (state.user) {
    const router = useRouter();
    router.push("/login");
  }
  if (authCode.value) {
    await githubhook(authCode.value);
  }
});
</script>
<template>
  <div class="col center my-8">
    <button class="rf x2" @click.prevent="signinWithPopup()">
      <Icon class="rf x2 cp scale sh" icon="logos:github-icon" />
    </button>
  </div>
</template>
