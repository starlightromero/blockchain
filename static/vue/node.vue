/*  global
    Vue, axios
*/

new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data: {
    blockchain: [],
    openTransactions: [],
    wallet: null,
    view: 'chain',
    walletLoading: false,
    txLoading: false,
    dataLoading: false,
    showElement: null,
    error: null,
    success: null,
    funds: 0,
    outgoingTx: {
      recipient: '',
      amount: 0
    }
  },
  computed: {
    loadedData: function () {
      if (this.view === 'chain') {
        return this.blockchain
      } else {
        return this.openTransactions
      }
    }
  },
  methods: {
    onCreateWallet: function () {
      var vm = this
      this.walletLoading = true
      axios.post('/wallet')
        .then(function (response) {
          vm.error = null
          vm.success = `Created Wallet!\n
          Public Key: ${response.data.public_key}\n
          Private Key: ${response.data.private_key}`
          vm.wallet = {
            public_key: response.data.public_key,
            private_key: response.data.private_key
          }
          vm.funds = response.data.funds
          vm.walletLoading = false
        })
        .catch(function (error) {
          vm.success = null
          vm.error = error.response.data.message
          vm.wallet = null
          vm.walletLoading = false
        })
    },
    onLoadWallet: function () {
      var vm = this
      this.walletLoading = true
      axios.get('/wallet')
        .then(function (response) {
          vm.error = null
          vm.success = `Loaded Wallet!\n
          Public Key: ${response.data.public_key}\n
          Private Key: ${response.data.private_key}`
          vm.wallet = {
            public_key: response.data.public_key,
            private_key: response.data.private_key
          }
          vm.funds = response.data.funds
          vm.walletLoading = false
        })
        .catch(function (error) {
          vm.success = null
          vm.error = error.response.data.message
          vm.wallet = null
          vm.walletLoading = false
        })
    },
    onSendTx: function () {
      this.txLoading = true
      var vm = this
      axios.post('/transaction', {
          recipient: this.outgoingTx.recipient,
          amount: this.outgoingTx.amount
        })
        .then(function (response) {
          vm.error = null
          vm.success = response.data.message
          console.log(response.data)
          vm.funds = response.data.funds
          vm.txLoading = false
        })
        .catch(function (error) {
          vm.success = null
          vm.error = error.response.data.message
          vm.txLoading = false
        })
    },
    onMine: function () {
      var vm = this
      axios.post('/mine')
        .then(function (response) {
          vm.error = null
          vm.success = response.data.message
          console.log(response.data)
          vm.funds = response.data.funds
        })
        .catch(function (error) {
          vm.success = null
          vm.error = error.response.data.message
        })
    },
    onResolve: function () {
      var vm = this
      axios.post('/resolve_conflicts')
        .then(function (response) {
          vm.error = null
          vm.success = response.data.message
        })
        .catch(function (error) {
          vm.success = null
          vm.error = error.response.data.message
        })
    },
    onLoadData: function () {
      if (this.view === 'chain') {
        var vm = this
        this.dataLoading = true
        axios.get('/chain')
          .then(function (response) {
            vm.blockchain = response.data
            vm.dataLoading = false
          })
          .catch(function (error) {
            vm.dataLoading = false
            vm.error = 'Something went wrong.'
          })
      } else {
        var vm = this
        axios.get('/transactions')
          .then(function (response) {
            vm.openTransactions = response.data
            vm.dataLoading = false
          })
          .catch(function (error) {
            vm.dataLoading = false
            vm.error = 'Something went wrong.'
          })
      }
    }
  }
})
