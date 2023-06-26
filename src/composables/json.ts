const loads = (data: any) => {
  if (typeof data === "string") return JSON.parse(data);
  else return data;
};

const dumps = (data: any) => {
  if (typeof data === "string") return data;
  else return JSON.stringify(data, null, 2);
};

export const useJson = () => ({
  loads,
  dumps,
});
