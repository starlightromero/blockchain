new Vue({
  el: '#app',
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
      // Send Http request to create a new wallet (and return keys)
      var vm = this
      this.walletLoading = true
      axios.post('/wallet')
        .then(function (response) {
          vm.error = null
          vm.success = 'Created Wallet! Public Key: ' + response.data.public_key + ', Private Key: ' + response.data.private_key
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
      // Send Http request to load an existing wallet (from a file on the server)
      var vm = this
      this.walletLoading = true
      axios.get('/wallet')
        .then(function (response) {
          vm.error = null
          vm.success = 'Created Wallet! Public Key: ' + response.data.public_key + ', Private Key: ' + response.data.private_key
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
      // Send Transaction to backend
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
    onLoadData: function () {
      if (this.view === 'chain') {
        // Load blockchain data
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
        // Load transaction data
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
