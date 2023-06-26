import { Request } from "~/types";
export const useRequest = () => {
  const data = ref<any | null>(null);
  const error = ref<any | null>(null);
  const loading = ref<boolean>(false);
  const request = async (request: Request): Promise<void> => {
    const {
      data: response,
      error: isError,
      isFetching,
    } = await useFetch(
      request.url,
      {
        method: request.method,
        headers: request.headers,
        body: request.body,
      },
      {
        refetch: request.refetch,
      }
    ).json();
    data.value = unref(response);
    error.value = isError.value;
    loading.value = isFetching.value;
  };
  return { data, request, error, loading };
};
