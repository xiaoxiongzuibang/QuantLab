// Identify Strategy Selected By Users
const StrategySelection = document.getElementById('strategy')
const DSMAOption = document.getElementById('dsmaoption')
const DEMAOption = document.getElementById('demaoption')
const MACDOption = document.getElementById('macdoption')

// Listen Strategy Selector
StrategySelection.addEventListener('change', function() {
    if (StrategySelection.value === "dema") {
        DEMAOption.classList.remove('hidden')
    }
    else if (StrategySelection.value === "dsma") {
        DSMAOption.classList.remove('hidden')
    }
    else if (StrategySelection.value === "MACD") {
        MACDOption.classList.remove('hidden')
}
})

// Theme Settings


