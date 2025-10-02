/*
<md-elevation part="elevation"></md-elevation>
<div class="background"></div>
<slot></slot>
<div class="outline"></div>
*/

class CustomCard extends HTMLElement {
  constructor() {
    super();

    // Attach shadow DOM
    const shadow = this.attachShadow({ mode: "open" });

    // Create and append the HTML structure
    const elevation = document.createElement("md-elevation");
    elevation.setAttribute("part", "elevation");

    const background = document.createElement("div");
    background.classList.add("background");

    const slot = document.createElement("slot");

    const outline = document.createElement("div");
    outline.classList.add("outline");

    shadow.appendChild(elevation);
    shadow.appendChild(background);
    shadow.appendChild(slot);
    shadow.appendChild(outline);

    // Apply styles from the host document
    const style = document.createElement("style");
    style.textContent = `
          :host {
            border-radius: var(--_container-shape);
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            position: relative;
            z-index: 0;
          }
          md-elevation,
          .background,
          .outline {
            border-radius: inherit;
            inset: 0;
            pointer-events: none;
            position: absolute;
          }
          .background {
            background: var(--_container-color);
            z-index: -1;
          }
          .outline {
            border: 1px solid transparent;
            z-index: 1;
          }
          md-elevation {
            z-index: -1;
            --md-elevation-level: var(--_container-elevation);
            --md-elevation-shadow-color: var(--_container-shadow-color);
          }
          slot {
            border-radius: inherit;
          }
          .outline {
            border-color: var(--_outline-color);
            border-width: var(--_outline-width);
          }
        `;
    shadow.appendChild(style);
  }
}

// Define the custom element
customElements.define("md-card", CustomCard);
