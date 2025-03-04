// Identify Strategy Selected By Users
const StrategySelection = document.getElementById('strategy')
const DSMAOption = document.getElementById('dsmaoption')
const DEMAOption = document.getElementById('demaoption')
// const MACDOption = document.getElementById('macdoption')
const ObjList = [DSMAOption, DEMAOption]
const Parameters = document.getElementById('parameters')
const GenerateButton = document.getElementById('generate button')

// Listen Strategy Selector
StrategySelection.addEventListener('change', function() {
    for (let obj of ObjList) {
        obj.classList.remove('display')
        obj.classList.add('hidden')
    }
    if (StrategySelection.value === "dema") {
        DEMAOption.classList.remove('hidden')
        DEMAOption.classList.add('display')
        }

    else if (StrategySelection.value === "dsma") {
        DSMAOption.classList.remove('hidden')
        DSMAOption.classList.add('display')
    }
    // else if (StrategySelection.value === "macd") {
    //     MACDOption.classList.remove('hidden')
    //     MACDOption.classList.add('display')
    // }
})

// Listen Generate Button
GenerateButton.addEventListener('click', function() {
    Parameters.classList.add('hidden')
})


