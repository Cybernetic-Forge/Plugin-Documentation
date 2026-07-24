(() => {
  "use strict";

  if (document.querySelector(".cf-arcane-background")) {
    return;
  }

  const main = document.querySelector(".md-main");
  if (!main) {
    return;
  }

  const polar = (radius, angle) => {
    const radians = (angle - 90) * Math.PI / 180;
    return [
      (radius * Math.cos(radians)).toFixed(2),
      (radius * Math.sin(radians)).toFixed(2),
    ];
  };

  const polygon = (sides, radius, offset = 0) =>
    Array.from({ length: sides }, (_, index) =>
      polar(radius, offset + index * 360 / sides).join(",")
    ).join(" ");

  const ticks = Array.from({ length: 72 }, (_, index) => {
    const major = index % 6 === 0;
    const medium = index % 3 === 0;
    const outer = polar(458, index * 5);
    const inner = polar(major ? 428 : medium ? 438 : 445, index * 5);
    return `<line x1="${inner[0]}" y1="${inner[1]}" x2="${outer[0]}" y2="${outer[1]}" stroke-width="${major ? 2 : 0.8}" opacity="${major ? 0.95 : medium ? 0.72 : 0.42}" />`;
  }).join("");

  const spokes = Array.from({ length: 24 }, (_, index) => {
    const outer = polar(index % 2 ? 355 : 375, index * 15);
    const inner = polar(index % 2 ? 182 : 206, index * 15);
    return `<line x1="${inner[0]}" y1="${inner[1]}" x2="${outer[0]}" y2="${outer[1]}" stroke-width="0.8" opacity="${index % 2 ? 0.36 : 0.62}" />`;
  }).join("");

  const nodes = Array.from({ length: 12 }, (_, index) => {
    const point = polar(394, index * 30);
    const rotation = index * 30;
    return `
      <g transform="translate(${point[0]} ${point[1]}) rotate(${rotation})">
        <circle r="18" stroke-width="1" />
        <circle r="12" stroke-dasharray="2 4" stroke-width="0.8" />
        <path d="M 0 -11 L 7 0 L 0 11 L -7 0 Z M -11 0 H 11 M 0 -15 V 15" stroke-width="0.9" />
        <circle r="2.2" fill="currentColor" stroke="none" />
      </g>`;
  }).join("");

  const petals = Array.from({ length: 16 }, (_, index) =>
    `<ellipse cx="0" cy="-117" rx="26" ry="104" transform="rotate(${index * 22.5})" stroke-width="0.75" opacity="0.48" />`
  ).join("");

  const layer = document.createElement("div");
  layer.className = "cf-arcane-background";
  layer.setAttribute("aria-hidden", "true");
  layer.innerHTML = `
    <svg viewBox="-520 -520 1040 1040" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">
      <g class="cf-arcane__pulse">
        <circle r="486" stroke-width="0.7" opacity="0.22" />
        <circle r="472" stroke-width="1.1" stroke-dasharray="1 9" opacity="0.62" />
        <circle r="458" stroke-width="0.9" />
        ${ticks}
      </g>

      <g class="cf-arcane__orbit--outer">
        <circle r="423" stroke-width="1.1" stroke-dasharray="94 13 4 13" />
        <circle r="410" stroke-width="0.65" stroke-dasharray="2 7" />
        <polygon points="${polygon(12, 394, 15)}" stroke-width="0.8" opacity="0.54" />
        <polygon points="${polygon(6, 380)}" stroke-width="1.15" />
        <polygon points="${polygon(6, 380, 30)}" stroke-width="1.15" />
        ${nodes}
      </g>

      <g opacity="0.72">
        <circle r="362" stroke-width="0.8" />
        <circle r="345" stroke-width="1" stroke-dasharray="18 6 2 6" />
        ${spokes}
        <polygon points="${polygon(8, 318, 22.5)}" stroke-width="0.75" />
        <polygon points="${polygon(4, 304, 45)}" stroke-width="1.05" />
        <polygon points="${polygon(4, 304)}" stroke-width="1.05" />
      </g>

      <g class="cf-arcane__orbit--inner">
        <circle r="278" stroke-width="1" stroke-dasharray="54 7 3 7" />
        <circle r="254" stroke-width="0.75" stroke-dasharray="2 8" />
        <polygon points="${polygon(12, 246)}" stroke-width="0.7" opacity="0.65" />
        <polygon points="${polygon(3, 232)}" stroke-width="1.25" />
        <polygon points="${polygon(3, 232, 60)}" stroke-width="1.25" />
        <polygon points="${polygon(3, 232, 30)}" stroke-width="0.65" opacity="0.56" />
        <polygon points="${polygon(3, 232, 90)}" stroke-width="0.65" opacity="0.56" />
      </g>

      <g opacity="0.68">
        ${petals}
        <circle r="174" stroke-width="0.8" />
        <circle r="146" stroke-width="1.1" stroke-dasharray="5 7" />
        <polygon points="${polygon(8, 132, 22.5)}" stroke-width="0.9" />
        <polygon points="${polygon(4, 112, 45)}" stroke-width="1.2" />
        <circle r="92" stroke-width="0.75" />
        <path d="M 0 -82 L 22 -22 L 82 0 L 22 22 L 0 82 L -22 22 L -82 0 L -22 -22 Z" stroke-width="1.1" />
        <circle r="50" stroke-width="0.8" stroke-dasharray="1 5" />
        <path d="M 0 -42 L 36 21 L -36 21 Z M 0 42 L 36 -21 L -36 -21 Z" stroke-width="1.1" />
        <circle r="13" stroke-width="1.2" />
        <circle r="4" fill="currentColor" stroke="none" />
      </g>

      <g stroke-width="0.7" opacity="0.38">
        <path d="M -472 0 H -362 M 362 0 H 472 M 0 -472 V -362 M 0 362 V 472" />
        <path d="M -334 -334 L -265 -265 M 265 265 L 334 334 M 334 -334 L 265 -265 M -265 265 L -334 334" />
        <circle cx="-334" cy="-334" r="8" />
        <circle cx="334" cy="-334" r="8" />
        <circle cx="334" cy="334" r="8" />
        <circle cx="-334" cy="334" r="8" />
      </g>
    </svg>`;
  main.prepend(layer);

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (reducedMotion.matches) {
    return;
  }

  let targetX = 0;
  let targetY = 0;
  let currentX = 0;
  let currentY = 0;
  let frame = 0;

  const render = () => {
    currentX += (targetX - currentX) * 0.065;
    currentY += (targetY - currentY) * 0.065;
    layer.style.setProperty("--cf-arcane-x", `${currentX.toFixed(2)}px`);
    layer.style.setProperty("--cf-arcane-y", `${currentY.toFixed(2)}px`);
    layer.style.setProperty("--cf-arcane-tilt", `${(currentX * -0.018).toFixed(3)}deg`);

    if (Math.abs(targetX - currentX) > 0.02 || Math.abs(targetY - currentY) > 0.02) {
      frame = requestAnimationFrame(render);
    } else {
      frame = 0;
    }
  };

  const moveTo = (x, y) => {
    targetX = -((x / window.innerWidth) - 0.5) * 34;
    targetY = -((y / window.innerHeight) - 0.5) * 26;
    if (!frame) {
      frame = requestAnimationFrame(render);
    }
  };

  window.addEventListener("pointermove", (event) => moveTo(event.clientX, event.clientY), { passive: true });
  document.documentElement.addEventListener("mouseleave", () => moveTo(window.innerWidth / 2, window.innerHeight / 2));
})();
