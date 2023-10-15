<script>
  export let repos = [];

  const formatCreatedDate = (createdAt) => {
    const date = new Date(createdAt);
    const month = date.toLocaleString("default", { month: "short" });
    const year = date.getFullYear();
    return `${month} ${year}`;
  };

  const formatUpdatedDate = (updatedAt) => {
    const seconds = Math.floor(
    (new Date().getTime() - new Date(updatedAt).getTime()) / 1000
    );
    const intervals = [31536000, 2592000, 86400, 3600, 60];
    const intervalNames = ['year', 'month', 'day', 'hour', 'minute'];

    for (let i = 0; i < intervals.length; i++) {
      const interval = Math.floor(seconds / intervals[i]);
      if (interval >= 1) {
        return `${interval} ${intervalNames[i]}${interval > 1 ? 's' : ''} ago`;
      }
    }
    return `${Math.floor(seconds)} seconds ago`;
  };

  const makeTitle = (repo) => {
    return `${repo.name} is a ${repo.language} project by @${repo.owner.login} `
    + `on GitHub with ${repo.watchers_count} watchers`;
  }

</script>

{#if repos.length > 0}
  <ul>
    {#each repos as repo, index}
      <li title={makeTitle(repo)}>
        <a class="repo-name" href={repo.html_url} title={repo.full_name} target="_blank">
          <img src={repo.owner.avatar_url} width="28" height="28" />
          <span>{repo.owner.login}</span>/<span>{repo.name}</span>
        </a>
        {#if repo.description}
          <p class="repo-description">{repo.description}</p>
        {/if}
        <p class="repo-dates">
          <span>Created {formatCreatedDate(repo.created_at)}</span>
          <span>Updated {formatUpdatedDate(repo.updated_at)}</span>
        </p>

        <p class="repo-stats">
          <span class="star-count"><b>★</b> {repo.stargazers_count}</span>
          {#if repo.license}
            <span class="license">{repo.license.name}</span>
          {/if}
        </p>

        {#if repo.homepage }
          <a class="repo-homepage" href={repo.homepage} target="_blank">{repo.homepage}</a>
        {/if}
      </li>
    {/each}
  </ul>
{:else}
  <p>Nothing</p>
{/if}


<style lang="scss">
  ul {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
    list-style: none;
    gap: 1rem;
    padding: 0;
    margin: 1rem auto;
    li {
      background: var(--neutral-background);
      border-radius: 4px;
      padding: 0.25rem 0.5rem;

      display: flex;
      flex-direction: column;
      justify-content: space-around;
      .repo-name {
        font-size: 1.2rem;
        font-weight: bold;
        color: var(--primary);
        display: flex;
        gap: 0.25rem;
        text-decoration: none;
        text-overflow: ellipsis;
        overflow: hidden;
        white-space: nowrap;
        img {
          border-radius: 50%;
          margin-right: 0.25rem;
        }
      }
      .repo-description {
        margin: 0.5rem 0;
        font-size: 1rem;
        font-style: italic;
        opacity: 0.8;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;  
        overflow: hidden;
      }
      .repo-dates, .repo-stats {
        font-size: 0.8rem;
        opacity: 0.8;
        text-transform: uppercase;
        font-family: monospace;
        display: flex;
        span:not(:last-child) {
          margin-right: 1rem;
        }
        .star-count {
          b { font-size: 2rem; line-height: 1rem; }
        }
        .license {
          border: 1px solid var(--font-color-pale);
          border-radius: 4px;
          padding: 0 0.2rem;
          max-width: 148px;
          display: inline-block;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
      }
      .repo-homepage {
        margin: 0;
        font-size: 0.8rem;
        opacity: 0.8;
      }
    }
  }
</style>
