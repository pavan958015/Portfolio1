# Personal Portfolio - Pavan Soni

Welcome to my personal portfolio website! This modern, premium, glassmorphic portfolio showcases my skills, experience, projects, coding profiles, and contact details in a fully responsive layout.

Live Site: [pavan958015.github.io/Portfolio1/](https://pavan958015.github.io/Portfolio1/)

---

## ✨ Features

- 🌓 **Dynamic Theme Switcher**: Full Light Mode & Dark Mode toggling, with user preferences persisted using HTML5 `localStorage`.
- 🔮 **Glassmorphism Design**: High-end translucent cards (`backdrop-filter`) with subtle glowing borders and micro-interactions on hover.
- 🛠️ **Badges-Based Skills Grid**: Tech skills displayed with qualitative levels (e.g., Expert, Advanced) and interactive sub-tech tag badges instead of numerical percentage bars.
- 📐 **Equal Height Layouts**: Responsive grids engineered with Flexbox to ensure cards in the Expertise, Projects, and Internships sections maintain consistent heights.
- ✉️ **Google Sheets Form Integration**: Fully functional contact form and modal fields that post entries directly to Google Sheets using Apps Script.
- 📱 **Fully Responsive**: Optimized for seamless viewing on all device types (mobile, tablet, desktop).

---

## 🛠️ Technologies Used

- **HTML5**: Structured semantic markup.
- **CSS3 (Custom Properties)**: Vanilla CSS variable design system, transitions, grid/flex layouts, and glassmorphic designs.
- **Bootstrap 5**: Responsive layout grids and modal components.
- **JavaScript (ES6+)**: Custom theme toggle controller, scroll triggers, and DOM manipulation.
- **AOS (Animate On Scroll) Library**: Dynamic fade-in animations as visitors scroll down.

---

## 📁 Repository Structure

```graphql
portfolio-website/  
├── index.html              # Main page markup
├── css/  
│   └── style.css           # Premium theme variables & styles
├── js/  
│   ├── script.js           # Theme toggle & interaction script
│   └── script1.js          # Google Sheets contact form handler
├── images/                 # Optimized project icons & assets
├── PDFs/  
│   └── Java_Full_Stack_Developer.pdf   # Resume document
└── ReadMe.md               # Project documentation  
```

---

## 🚀 Getting Started

### Prerequisites
To run this project locally, you only need:
- A modern web browser (e.g., Google Chrome, Firefox, Safari).
- A code editor (e.g., VS Code) for modifications.

### Running Locally
1. Clone this repository:
   ```bash
   git clone https://github.com/pavan958015/Portfolio1.git
   ```
2. Navigate into the project folder:
   ```bash
   cd Portfolio1
   ```
3. Open `index.html` in your browser. (Or use a local development server like VS Code "Live Server").

---

## 🎨 Customization & Maintenance

### Theme Modifications
The stylesheet is built entirely on custom variables. You can easily tweak the color scheme under `:root` and `body.light-theme` inside [style.css](file:///c:/Users/Pavan Soni/Downloads/Portfolio1-main (2)/Portfolio1-main/css/style.css):
```css
:root {
    --bg-primary: #090816;
    --icon-color: #6366f1;
    /* ... add your custom colors here ... */
}
```

### Adding New Project Cards
To add a new project, edit [index.html](file:///c:/Users/Pavan Soni/Downloads/Portfolio1-main (2)/Portfolio1-main/index.html) and add a column item in the `#portfolio` section:
```html
<div class="post col-md-4 web website all col-10 mt-3 mt-md-0" data-aos="fade-up">
  <div class="card">
    <img src="images/your-thumbnail.webp" class="card-img-top" alt="..." />
    <div class="card-body text-center">
      <h4 class="card-title">Project Title</h4>
      <div class="project-tags">
        <span class="badge">Tag 1</span>
        <span class="badge">Tag 2</span>
      </div>
      <div class="project-links">
        <a href="#" class="link" target="_blank">View on GitHub</a>
      </div>
    </div>
  </div>
</div>
```
