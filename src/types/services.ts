export interface Request {
  url: string;
  method?: string;
  headers?: Record<string, string>;
  body?: string | File | FormData | ReadableStream | null;
  refetch?: boolean;
}

export interface GithubRepo {
  name: string;
  full_name: string;
  private: boolean;
  html_url: string;
  description?: string;
  fork: boolean;
  url: string;
  created_at: string;
  updated_at: string;
  pushed_at: string;
  homepage?: string;
  size: number;
  stargazers_count: number;
  watchers_count: number;
  language?: string;
  forks_count: number;
  open_issues_count: number;
  master_branch?: string;
  default_branch: string;
  score: number;
}

export interface Owner {
  login: string;
  id: number;
  node_id: string;
  avatar_url: string;
  gravatar_id: string | null;
  url: string;
  html_url: string;
  followers_url: string;
  following_url: string;
  gists_url: string;
  starred_url: string;
  subscriptions_url: string;
  organizations_url: string;
  repos_url: string;
  events_url: string;
  received_events_url: string;
  type: string;
  site_admin: boolean;
}

export interface Permissions {
  admin: boolean;
  maintain: boolean;
  push: boolean;
  triage: boolean;
  pull: boolean;
}

export interface GithubFullRepo {
  id: number;
  node_id: string;
  name: string;
  full_name: string;
  private: boolean;
  owner: Owner;
  html_url: string;
  description: string | null;
  fork: boolean;
  url: string;
  forks_url: string | null;
  keys_url: string | null;
  collaborators_url: string | null;
  teams_url: string | null;
  hooks_url: string | null;
  issue_events_url: string | null;
  events_url: string | null;
  assignees_url: string | null;
  branches_url: string | null;
  tags_url: string | null;
  blobs_url: string | null;
  git_tags_url: string | null;
  git_refs_url: string | null;
  trees_url: string | null;
  statuses_url: string | null;
  languages_url: string | null;
  stargazers_url: string | null;
  contributors_url: string | null;
  subscribers_url: string | null;
  subscription_url: string | null;
  commits_url: string;
  git_commits_url: string;
  comments_url: string | null;
  issue_comment_url: string | null;
  contents_url: string;
  compare_url: string | null;
  merges_url: string | null;
  archive_url: string | null;
  downloads_url: string | null;
  issues_url: string | null;
  pulls_url: string | null;
  milestones_url: string | null;
  notifications_url: string | null;
  labels_url: string | null;
  releases_url: string | null;
  deployments_url: string | null;
  created_at: string;
  updated_at: string;
  pushed_at: string;
  git_url: string;
  ssh_url: string;
  clone_url: string;
  svn_url: string;
  homepage: string | null;
  size: number;
  stargazers_count: number;
  watchers_count: number;
  language: string | null;
  has_issues: boolean;
  has_projects: boolean;
  has_downloads: boolean;
  has_wiki: boolean;
  has_pages: boolean;
  has_discussions: boolean;
  forks_count: number;
  mirror_url: string | null;
  archived: boolean;
  disabled: boolean;
  open_issues_count: number;
  license: string | null;
  allow_forking: boolean;
  is_template: boolean;
  web_commit_signoff_required: boolean;
  topics: string[];
  visibility: string;
  forks: number;
  open_issues: number;
  watchers: number;
  default_branch: string;
  permissions: Permissions;
  allow_squash_merge: boolean;
  allow_merge_commit: boolean;
  allow_rebase_merge: boolean;
  allow_auto_merge: boolean;
  delete_branch_on_merge: boolean;
  allow_update_branch: boolean;
  use_squash_pr_title_as_default: boolean;
  squash_merge_commit_message: string;
  squash_merge_commit_title: string;
  merge_commit_message: string;
  merge_commit_title: string;
  network_count: number;
  subscribers_count: number;
}

export interface ContainerCreate {
  login: string;
  repo: string;
  token: string;
  email: string;
  image: string;
}

export interface RepoTemplateCreate {
  template_owner: string;
  template_repo: string;
  name: string;
  description?: string;
  private?: boolean;
  login: string;
  token: string;
  email: string;
}
