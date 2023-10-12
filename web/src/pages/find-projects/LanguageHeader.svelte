<script>
  export let language = {};

  const iconUrl = (icon) => {
    const iconSize = 48;
    const iconColor = '161618';
    return `https://api.iconify.design/${icon}.svg?height=${iconSize}&color=%23${iconColor}`;
  };

</script>

<header style={`background: ${language.color}`}>
  <img src={iconUrl(language.icon)} />
  <h2>{language.name}</h2>
</header>

<p class="intro">
  The following {language.name} projects have been tagged
  as welcoming for first-time contributors.
</p>

<style lang="scss">
header {
  border-radius: 4px;
  padding: 1rem 2rem;
  color: var(--background);
  display: flex;
  gap: 1rem;
}

.intro {
  margin: 0.5rem 0;
  color: var(--font-color-pale);
  font-style: italic;
}
</style>
