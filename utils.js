async function saveConfig(config) {
  const token = 'ghp_YOUR_GITHUB_PAT'; // use GitHub Secret in prod
  await fetch('https://api.github.com/gists/cc77ca8c82ed2627b2ea5d57e4743efa', {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `token ${token}`
    },
    body: JSON.stringify({
      files: {
        'config.json': {
          content: JSON.stringify(config, null, 2)
        }
      }
    })
  });
}
