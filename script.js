// Alonda Gallery — 10 portraits
const SHOTS = [
  // Tier 1 — the original 10
  { file: 'assets/images/01_beach_bikini.jpeg', label: 'Bikini · Playa' },
  { file: 'assets/images/02_black_dress.jpeg', label: 'Vestido negro · Gala' },
  { file: 'assets/images/03_red_evening.jpeg', label: 'Vestido rojo · Noche' },
  { file: 'assets/images/04_gym_sporty.jpeg', label: 'Look gym · Fit' },
  { file: 'assets/images/05_casual_denim.jpeg', label: 'Casual · Jeans & top' },
  { file: 'assets/images/06_loungewear_home.jpeg', label: 'Loungewear · Hogar' },
  { file: 'assets/images/07_pool_party.jpeg', label: 'Traje de baño · Pool party' },
  { file: 'assets/images/08_office_pro.jpeg', label: 'Oficina · Profesional' },
  { file: 'assets/images/09_beach_coverup.jpeg', label: 'Túnica · Beach cover-up' },
  { file: 'assets/images/10_casual_selfie.jpeg', label: 'Selfie · Casual chic' },
  // Tier 2 — 10 nuevas
  { file: 'assets/images/11_golden_hour_selfie.jpeg', label: 'Golden hour · Selfie' },
  { file: 'assets/images/12_pink_floral_dress.jpeg', label: 'Vestido floral rosa' },
  { file: 'assets/images/13_magazine_cover.jpeg', label: 'Magazine cover · Esmeralda' },
  { file: 'assets/images/14_white_sundress.jpeg', label: 'White sundress · Tropical' },
  { file: 'assets/images/15_cocktail_bar.jpeg', label: 'Cocktail bar · Plata' },
  { file: 'assets/images/16_concert_festival.jpeg', label: 'Festival · Concierto' },
  { file: 'assets/images/17_library_cozy.jpeg', label: 'Library · Cozy chic' },
  { file: 'assets/images/18_brunch_aesthetic.jpeg', label: 'Brunch · Aesthetic' },
  { file: 'assets/images/19_salsa_dancing.jpeg', label: 'Salsa · Baile mexicano' },
  { file: 'assets/images/20_rooftop_night.jpeg', label: 'Rooftop night · Ciudad' },
  // Tier 3A · Editorial / Moda
  { file: 'assets/images/21_wedding_dress.jpeg', label: 'Wedding dress · Novia' },
  { file: 'assets/images/22_power_suit.jpeg', label: 'Power suit · Ejecutiva' },
  { file: 'assets/images/23_minimalist_studio.jpeg', label: 'Minimalist · Studio' },
  { file: 'assets/images/24_boho_crochet.jpeg', label: 'Boho crochet · Beach' },
  { file: 'assets/images/25_couture_runway.jpeg', label: 'Couture · Runway' },
  // Tier 3B · Cultura / Lifestyle
  { file: 'assets/images/26_paris_cafe.jpeg', label: 'Café parisino' },
  { file: 'assets/images/27_skate_park.jpeg', label: 'Skate park · Urbana' },
  { file: 'assets/images/28_art_museum.jpeg', label: 'Museo de arte' },
  { file: 'assets/images/29_train_station.jpeg', label: 'Estación de tren' },
  { file: 'assets/images/30_sunrise_rooftop.jpeg', label: 'Amanecer · Rooftop' },
  // Tier 3C · México lindo
  { file: 'assets/images/31_tehuana_oaxaquena.jpeg', label: 'Tehuana · Oaxaqueña' },
  { file: 'assets/images/32_catrina_dia_muertos.jpeg', label: 'Catrina · Día de muertos' },
  { file: 'assets/images/33_flower_market.jpeg', label: 'Mercado de flores' },
  { file: 'assets/images/34_charra_sombrero.jpeg', label: 'Charra · Sombrero' },
  { file: 'assets/images/35_frida_inspired.jpeg', label: 'Frida-inspired' },
  // Tier 3D · Deportes / Aventura
  { file: 'assets/images/36_surf_malibu.jpeg', label: 'Surf · Malibu' },
  { file: 'assets/images/37_ski_aspen.jpeg', label: 'Esquí · Aspen' },
  { file: 'assets/images/38_yoga_mat.jpeg', label: 'Yoga mat' },
  { file: 'assets/images/39_boxing_training.jpeg', label: 'Boxeo · Training' },
  { file: 'assets/images/40_cycling_urban.jpeg', label: 'Ciclismo urbano' },
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