<script>
  export let languages = [];

  const iconUrl = (icon) => {
    const iconSize = 48;
    const iconColor = 'ffffff';
    return `https://api.iconify.design/${icon}.svg?height=${iconSize}&color=%23${iconColor}`;
  };

</script>
  
<section>
  <h1>Pick a language, any language</h1>
  <p class="intro">
    Choose a programming language below, to see a list of repositories
    that have been as marked as welcoming for first-time contributors.
  </p>
  <ul>
  {#each languages as language}
    <li style={`--language-color: ${language.color}`}>
      <a href={`/find-projects/${language.identifier}`}>
      <img src={iconUrl(language.icon)} />
      <h2>{language.name}</h2>
      </a>
    </li>
  {/each}
  </ul>
</section>

<style lang="scss">

section {
  max-width: 90vw;
  margin: 1rem auto;
  h1 {
    margin: 0.5rem 0;
  }
  .intro {
    color: var(--font-color-pale);
    margin: 0.5rem 0;
  }
}

ul {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}

a {
  text-decoration: none;
  cursor: pointer;
  display: flex;
  gap: 1rem;
  color: var(--font-color);
  border: 2px solid var(--language-color);
  border-radius: 4px;
  transition: 0.15s all ease-in-out;
  background: rgba(127,127,127,0.1);
  h2 {
    color: var(--font-color);
    transition: 0.15s all ease-in-out;
  }
  img {
    padding: 0.25rem;
    background: var(--language-color);
    transition: 0.15s all ease-in-out;
  }
  &:hover {
    background: var(--language-color);
    h2 {
      transform: translateX(0.5rem)
    }
  }
}
</style>
