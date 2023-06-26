export const useAuth = () => {
  const response = ref<any>(null);
  const { state } = useStore();
  const loginWithGithub = async (code: string) => {
    const { data } = await useFetch("/api/github", {
      method: "POST",
      body: JSON.stringify({ code }),
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${state.token}`
      }
    }).json();

    return unref(data);
  };

  const GIHUB_URL =
    "https://github.com/login/oauth/authorize?client_id=00fc60bdaf14af17bf6f&redirect_uri=http://localhost:3000/login&scope=user,repo";

  const signinWithPopup = () => {
    window.location.href = GIHUB_URL;
  };

  watch(response, (res) => {
    if (res) {
        response.value = res;
    }
  });

  return {
    response,
    signinWithPopup,
    loginWithGithub,
  };
};
