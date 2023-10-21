
import fetch from 'node-fetch';
import { languages, repoTags } from './languages';

type SortMethod = 'popular' | 'forks' | 'most_help_wanted' | 'recently_updated';

const API_KEY = process.env.GH_ACCESS_TOKEN;

export const getStaticPaths = async () => {
  const sortMethods: SortMethod[] = ['popular', 'forks', 'most_help_wanted', 'recently_updated'];

  const paths: object[] = [];

  languages.forEach((lang) => {
    sortMethods.forEach((method) => {
      paths.push({ params: { language: lang.identifier, sort: method } });
    });
  });
  return paths;
}


// Fetch repositories based on language and topics
export async function fetchRepos(lang) {
    if (!lang || !API_KEY) {
        throw new Error("Both language and API_KEY are required.");
    }

    const TIMEOUT = 10000;
    const fetchedRepos = new Set();
    const combinedRepos = [];
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), TIMEOUT);

    const sortStrategy: { [key in SortMethod]: string } = {
        'popular': 'stars',
        'forks': 'forks',
        'most_help_wanted': 'help-wanted-issues',
        'recently_updated': 'updated'
    };

    for (const topic of repoTags) {
        const url = `https://api.github.com/search/repositories?q=language`
        + `:${lang}+topic:${topic}&sort=stars&order=desc`;

        try {
            const response = await fetch(url, {
                headers: {
                    'Authorization': `token ${API_KEY}`,
                    'Accept': 'application/vnd.github.mercy-preview+json'
                },
                signal: controller.signal
            });

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
            throw error;
        }
    }

    clearTimeout(timeoutId);
    return combinedRepos.sort((a, b) => b.stargazers_count - a.stargazers_count);
}



