// Alonda Gallery — 10 portraits
const SHOTS = [
  { file: 'assets/images/01_bikini_playa.jpeg', label: 'Bikini · Playa' },
  { file: 'assets/images/02_vestido_negro.jpeg', label: 'Vestido negro · Gala' },
  { file: 'assets/images/03_vestido_rojo.jpeg', label: 'Vestido rojo · Noche' },
  { file: 'assets/images/04_gym_fit.jpeg', label: 'Look gym · Fit' },
  { file: 'assets/images/05_casual_jeans.jpeg', label: 'Casual · Jeans & top' },
  { file: 'assets/images/06_loungewear.jpeg', label: 'Loungewear · Hogar' },
  { file: 'assets/images/07_pool_party.jpeg', label: 'Traje de baño · Pool party' },
  { file: 'assets/images/08_oficina_profesional.jpeg', label: 'Oficina · Profesional' },
  { file: 'assets/images/09_beach_coverup.jpeg', label: 'Túnica · Beach cover-up' },
  { file: 'assets/images/10_selfie_chic.jpeg', label: 'Selfie · Casual chic' },
];

const gallery = document.getElementById('gallery');
const lightbox = document.createElement('div');
lightbox.className = 'lightbox';
document.body.appendChild(lightbox);

const lbImg = document.createElement('img');
lightbox.appendChild(lbImg);

lightbox.addEventListener('click', () => lightbox.classList.remove('open'));

document.addEventListener('keydown', e => {
  if (e.key === 'Escape') lightbox.classList.remove('open');
});

SHOTS.forEach(shot => {
  const card = document.createElement('article');
  card.className = 'card';
  card.innerHTML = `
    <img src="${shot.file}" alt="${shot.label}" loading="lazy" />
    <div class="card-label">${shot.label}</div>
  `;
  card.addEventListener('click', () => {
    lbImg.src = shot.file;
    lbImg.alt = shot.label;
    lightbox.classList.add('open');
  });
  gallery.appendChild(card);
});