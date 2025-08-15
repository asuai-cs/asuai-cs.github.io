
// Smooth scrolling for navigation links (only for hash links)
document.querySelectorAll('nav a').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href.startsWith('#')) {
            e.preventDefault();
            const targetId = href;
            document.querySelector(targetId).scrollIntoView({ behavior: 'smooth' });
        }
        // Non-hash links (like cv.html) will navigate normally
    });
});

// Hover effect on sections
const sections = document.querySelectorAll('section');
sections.forEach(section => {
    section.addEventListener('mouseover', () => {
        section.style.backgroundColor = '#e8ecef';
        section.style.boxShadow = '0 4px 10px rgba(0, 0, 0, 0.2)';
    });
    section.addEventListener('mouseout', () => {
        section.style.backgroundColor = 'white';
        section.style.boxShadow = '0 2px 5px rgba(0, 0, 0, 0.1)';
    });
});

// Simulated visitor counter
let visitorCount = localStorage.getItem('visitorCount') ? parseInt(localStorage.getItem('visitorCount')) : 0;
visitorCount++;
localStorage.setItem('visitorCount', visitorCount);
const visitorCountElement = document.getElementById('visitor-count');
if (visitorCountElement) {
    visitorCountElement.textContent = visitorCount;
} else {
    console.error('Visitor count element not found');
}

// Mobile menu toggle
const navUl = document.querySelector('nav ul');
const hamburger = document.createElement('div');
hamburger.className = 'hamburger';
hamburger.innerHTML = '☰';
hamburger.style.display = 'none';
hamburger.style.cursor = 'pointer';
hamburger.style.color = 'white';
hamburger.style.fontSize = '24px';
hamburger.style.padding = '10px';
document.querySelector('nav').prepend(hamburger);

hamburger.addEventListener('click', () => {
    navUl.style.display = navUl.style.display === 'none' ? 'block' : 'none';
});

window.addEventListener('resize', () => {
    if (window.innerWidth <= 600) {
        hamburger.style.display = 'block';
        navUl.style.display = 'none';
    } else {
        hamburger.style.display = 'none';
        navUl.style.display = 'flex';
    }
});

window.dispatchEvent(new Event('resize'));

// Timeline animation
const timelineItems = document.querySelectorAll('.timeline-item');
const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, { threshold: 0.1 });

timelineItems.forEach(item => {
    item.style.opacity = '0';
    item.style.transform = 'translateY(20px)';
    observer.observe(item);
});

// Skills tree animation
const subBranches = document.querySelectorAll('.sub-branch');
const skillsObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            subBranches.forEach((branch, index) => {
                setTimeout(() => {
                    branch.classList.add('animate');
                }, index * 100);
            });
            skillsObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.1 });

const skillsTree = document.querySelector('.skills-tree');
if (skillsTree) {
    skillsObserver.observe(skillsTree);
}

// Back to top button
const backToTopButton = document.getElementById('back-to-top');
window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        backToTopButton.style.display = 'block';
    } else {
        backToTopButton.style.display = 'none';
    }
});
backToTopButton.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Modal functionality
document.querySelectorAll('.project-modal-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const modalId = btn.dataset.modal;
        const modal = document.getElementById(modalId);
        modal.classList.add('show');
        const tabContainer = modal.querySelector('.tab-container');
        if (tabContainer) {
            const tabs = tabContainer.querySelectorAll('.tab-btn');
            const contents = modal.querySelectorAll('.tab-content');
            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.style.display = 'none');
            tabs[0].classList.add('active');
            contents[0].style.display = 'block';
        }
    });
});

document.querySelectorAll('.close-modal').forEach(closeBtn => {
    closeBtn.addEventListener('click', () => {
        closeBtn.closest('.modal').classList.remove('show');
    });
});

document.querySelectorAll('.modal').forEach(modal => {
    modal.addEventListener('click', e => {
        if (e.target === modal) modal.classList.remove('show');
    });
});

// Tab switching
document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const modal = btn.closest('.modal-content');
        const tabId = btn.dataset.tab;
        const content = modal.querySelector(`#${tabId}`);
        modal.querySelectorAll('.tab-btn').forEach(t => t.classList.remove('active'));
        modal.querySelectorAll('.tab-content').forEach(c => c.style.display = 'none');
        btn.classList.add('active');
        content.style.display = 'block';
    });
});

// Highlight comments in code blocks
document.querySelectorAll('code.code-styled').forEach(codeBlock => {
    let code = codeBlock.innerHTML;
    code = code.replace(/(\/\/[^\n]*|(--[^\n]*))/g, '<span class="comment">$1</span>');
    code = code.replace(/(#[^\n]*)/g, '<span class="comment">$1</span>');
    codeBlock.innerHTML = code;
});

// Add to your existing modal handling
document.addEventListener('DOMContentLoaded', function() {
    const pchbModal = document.getElementById('pchb-modal');
    const pchbBtn = document.querySelector('[data-modal="pchb-modal"]');
    
    if (pchbBtn) {
        pchbBtn.addEventListener('click', function() {
            pchbModal.style.display = 'block';
        });
    }

    const closePchb = pchbModal.querySelector('.close-modal');
    closePchb.addEventListener('click', function() {
        pchbModal.style.display = 'none';
    });

    window.addEventListener('click', function(event) {
        if (event.target === pchbModal) {
            pchbModal.style.display = 'none';
        }
    });
});
