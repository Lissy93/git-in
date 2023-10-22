
import fetch from 'node-fetch';
import { languages, repoTags } from './languages';

type SortMethod = 'popular' | 'forks' | 'most-help-wanted' | 'recently-updated';

const API_KEY = process.env.GH_ACCESS_TOKEN;

export const getStaticPaths = async () => {
  const sortMethods: SortMethod[] = ['popular', 'forks', 'most-help-wanted', 'recently-updated'];

  const paths: object[] = [];

  languages.forEach((lang) => {
    sortMethods.forEach((method) => {
      paths.push({ params: { language: lang.identifier, sort: method } });
    });
  });
  return paths;
}

export async function fetchRepos(lang: string, sort: string) {
  if (!API_KEY) {
      throw new Error("You need to specify a GitHub PAT in the `GH_ACCESS_TOKEN` env var");
  }

  const TIMEOUT = 10000;
  const fetchedRepos = new Set();
  const combinedRepos = [];
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), TIMEOUT);

  const sortDict: { [key in SortMethod]: string } = {
      'popular': 'stars',
      'forks': 'forks',
      'most-help-wanted': 'help-wanted-issues',
      'recently-updated': 'updated'
  };

  const sortMethod = sortDict[sort];
  const sortOrder = 'desc';

  for (const topic of repoTags) {
      const url = 'https://api.github.com/search/repositories?q=language'
      + `:${lang}+topic:${topic}&sort=${sortMethod}&order=${sortOrder}`;

      try {
          const response = await fetch(url, {
              headers: {
                  'Authorization': `token ${API_KEY}`,
                  'Accept': 'application/vnd.github.mercy-preview+json'
              },
              signal: controller.signal
          });

          if (response.status === 403) {
              console.warn(`Rate limit hit for topic ${topic}`);
              continue; // Skip the current iteration, move on to the next topic
          }

          if (!response.ok) {
              throw new Error(`GitHub API returned ${response.status}: ${response.statusText}`);
          }

          const result = await response.json();
          for (const repo of result?.items || []) {
              if (!fetchedRepos.has(repo.id)) {
                  fetchedRepos.add(repo.id);
                  combinedRepos.push(repo);
              }
          }
      } catch (error) {
          if (error.name === 'AbortError') {
              throw new Error("Request timed out.");
          }
          console.error(`Error fetching for topic ${topic}: ${error.message}`);
      }
  }

  clearTimeout(timeoutId);


  let sortedRepos = combinedRepos;

  if (sort === 'recently-updated') {
    sortedRepos = combinedRepos.sort((a, b) => new Date(b.pushed_at).getTime() - new Date(a.pushed_at).getTime());
  } else if (sort === 'forks') {
    sortedRepos = combinedRepos.sort((a, b) => b.forks - a.forks);
  } else {
    sortedRepos = combinedRepos.sort((a, b) => b.stargazers_count - a.stargazers_count);
  }
  return sortedRepos;
}


