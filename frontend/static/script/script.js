// Identify Strategy Selected By Users
const StrategySelection = document.getElementById('strategy')
const Start = document.getElementById('start')
const End = document.getElementById('end')
let duration = Start - End

const DSMAOption = document.getElementById('dsmaoption')
const dsma_shortperiod = document.getElementById('stsmap')
const dsma_longperiod = document.getElementById('ltsmap')

const DEMAOption = document.getElementById('demaoption')
const dema_shortperiod = document.getElementById('stemap')
const dema_longperiod = document.getElementById('ltemap')

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

})

// Different Strategies requires minimum data
// For exemple, DSMAStrategy(5,20) requires at least 20 data
if (StrategySelection.value === 'dsma') {
    if (duration < dsma_longperiod) {
        alert('More data needed!')
    }
}
else if (StrategySelection.value === 'dema') {
    if (duration < dsma_longperiod) {
        alert('More data needed!')
    }
}

// Listen Generate Button
GenerateButton.addEventListener('click', function() {
    Parameters.classList.add('hidden')
})


