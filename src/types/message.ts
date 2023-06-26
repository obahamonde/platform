export type Message = {
  author: string;
  content: string;
  ref: string;
  ts: number;
};

export type Context = {
  key: string;
  value: string;
};
