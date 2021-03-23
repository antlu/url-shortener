function renderData(json) {
  const listOfURLs = document.querySelector('.list-of-urls');
  listOfURLs.innerHTML = '';
  json.forEach(link => {
    const p = document.createElement('p');
    const a = document.createElement('a');
    a.href = link.short_url;
    a.text = link.id;
    a.target = '_blank';
    text = document.createTextNode(` - ${link.original_url}`);
    p.appendChild(a);
    p.appendChild(text);
    listOfURLs.appendChild(p);
  });
}

function getData() {
  fetch('/api/')
  .then(response => response.json())
  .then(renderData);
}

const form = document.querySelector('.url-shortener');

form.addEventListener('submit', e => {
  e.preventDefault();
  fetch('/api/', {
    method: 'POST',
    body: new FormData(e.target),
  })
  .then(response => {
    if (response.ok) form.reset();
    if (response.status == 200) return { error: true, text: 'URL already in list' };
    if (response.status == 201) {
      getData();
      return { error: false, text: 'New URL added' };
    }
    return response.json();
  })
  .then(json => {
    const alert = document.querySelector('.alert');
    if (json.error) {
      alert.classList.remove('alert-success');
      alert.classList.add('alert-danger');
    } else {
      alert.classList.remove('alert-danger');
      alert.classList.add('alert-success');
    };
    alert.textContent = json.text;
  });
});

document.addEventListener('DOMContentLoaded', getData);
