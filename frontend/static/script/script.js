// Identify Strategy Selected By Users
const StrategySelection = document.getElementById('strategy')
const DSMAOption = document.getElementById('dsmaoption')
const DEMAOption = document.getElementById('demaoption')
// const Start = document.getElementById('start')
// const End = document.getElementById('end')

// const MACDOption = document.getElementById('macdoption')
const ObjList = [DSMAOption, DEMAOption]
const Parameters = document.getElementById('parameters')
const GenerateButton = document.getElementById('generatebutton')

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


// Listen Generate Button
GenerateButton.addEventListener('click', function() {
    
    // Different Strategies requires minimum data
    // For exemple, DSMAStrategy(5,20) requires at least 20 data
    const Start = document.getElementById('start')
    const End = document.getElementById('end')
    const StartStr = Start.value
    const EndStr = EndObj.value
    const StartDate = new Date(StartStr)
    const EndDate = new Date(EndStr)
    const diff1 = EndDate - StartDate
    const diff = diff1 / (3600*1000*24)

    if (StrategySelection.value === "dsma") {
        const dsma_longperiod = document.getElementById('ltsmap')
        if (diff < dsma_longperiod.value) {
            alert('More data needed!')
        }
        }
    else if (StrategySelection.value === "dema") {
        const dema_longperiod = document.getElementById('ltemap')
        if (diff < dema_longperiod.value) {
            alert('More data needed!')
        }
        }

})






