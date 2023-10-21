<script>
  export let language = {};

  const iconUrl = (icon) => {
    const iconSize = 48;
    const iconColor = '161618';
    return `https://api.iconify.design/${icon}.svg?height=${iconSize}&color=%23${iconColor}`;
  };

  const sortOptions =  ['popular', 'forks', 'most-help-wanted', 'recently-updated'];

</script>

<header style={`--language-color: ${language.color}`}>
  <div class="left">
    <img src={iconUrl(language.icon)} />
    <h2>{language.name}</h2>
  </div>
  <div class="right">
    <span>Sort by:</span>
    {#each sortOptions as option}
      <a href={`/find-projects/${language.identifier}/${option}`}>{option.replaceAll('-', ' ')}</a>
    {/each}
  </div>
</header>

<p class="intro">
  The following {language.name} projects have been tagged
  as welcoming for first-time contributors.
</p>

<style lang="scss">

.left {
  display: flex;
  gap: 1rem;
}

.right {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  a {
    color: var(--neutral-background);
    border: 1px solid var(--neutral-background);
    text-decoration: none;
    padding: 0.1rem 0.25rem;
    border-radius: 4px;
    transition: background 0.2s ease-in-out;
    text-transform: capitalize;
    &:hover {
      background: var(--neutral-background);
      color: var(--language-color);
    }
  }
}

header {
  border-radius: 4px;
  padding: 1rem 2rem;
  color: var(--background);
  background: var(--language-color);
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
}

.intro {
  margin: 0.5rem 0;
  color: var(--font-color-pale);
  font-style: italic;
}
</style>
