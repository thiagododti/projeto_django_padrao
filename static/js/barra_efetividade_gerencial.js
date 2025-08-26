document.querySelectorAll('.efetividade-bar').forEach((bar, index) => {
    const width = parseFloat(bar.dataset.width) || 0;
    const clampedWidth = Math.min(Math.max(width, 0), 100);

    // Define a cor baseada na porcentagem
    let colorClass = '';
    let textColorClass = '';

    if (width < 50) {
        colorClass = 'bg-red-500';
        textColorClass = 'text-red-600';
    } else if (width >= 50 && width < 80) {
        colorClass = 'bg-yellow-500';
        textColorClass = 'text-yellow-600';
    } else {
        colorClass = 'bg-green-500';
        textColorClass = 'text-green-600';
    }

    // Aplica a largura e a cor na barra
    bar.style.width = clampedWidth + '%';
    bar.className = `h-2 rounded-full efetividade-bar ${colorClass}`;

    // Aplica a cor no texto da porcentagem
    const textElement = document.querySelectorAll('.efetividade-text')[index];
    if (textElement) {
        textElement.className = `text-sm font-semibold efetividade-text ${textColorClass}`;
    }
});