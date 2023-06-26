export type User = {
  ref: string | undefined;
  ts: string | undefined;
  email: string | undefined;
  email_verified: boolean | undefined;
  family_name: string | undefined;
  given_name: string | undefined;
  locale: string | undefined;
  name: string;
  nickname: string | undefined;
  picture: string | undefined;
  sub: string;
  updated_at: string | undefined;
};

export interface UserLogin {
  username: string;
  password: string;
}

export interface UserSignUp {
  name: string;
  email: string;
  password: string;
  picture: string;
}
