<template>
  <base-app>
    <v-container
      fluid
    >
      <v-row
        align="center"
        justify="center"
      >
        <v-col
          cols="12"
        >
          <base-material-card
            icon="mdi-database-export"
          >
            <v-card-text>
              <v-row
                align="center"
                justify="center"
              >
                <v-col
                  cols="12"
                >
                  <v-form-base
                    id="exports"
                    :model="model"
                    :schema="schema"
                    @change:exports="log"
                    v-if="exportsFields"
                  >
                  </v-form-base>
                </v-col>
              </v-row>
              <v-row>
                <v-col
                  cols="1"
                >
                  <v-btn
                    large
                    color="green"
                    @click="export_data"
                  >
                    Kas
                  </v-btn>
                </v-col>
              </v-row>
            </v-card-text>
          </base-material-card>
        </v-col>
      </v-row>
      <v-row
      >
        <v-col
          cols="12"
          v-if="resultsData"
        >
          <v-simple-table>
            <thead>
              <tr>
                <th
                  v-for="(field, i) in model.fields.fields"
                  :key="i"
                  v-text="field"
                />
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(result, i) in resultsData"
                :key="i"
              >
                <td
                  v-for="(field, j) in result"
                  :key="j"
                  v-text="field"
                />
              </tr>
            </tbody>
          </v-simple-table>
        </v-col>
      </v-row>
    </v-container>
  </base-app>
</template>

<script>
  import { mapState } from 'vuex'
  import VFormBase from 'vuetify-form-base'
  import { log } from '../../../utils'

  export default {
    name: 'Home',
    components: { VFormBase },
    data () {
      return {
        operations: [0],
        orders: [0],
        model: {
          fields: {
            fields: [],
          },
          operations: this.newOperationModel(0),
          orders: this.newOrderModel(0),
        },
      }
    },
    computed: {
      ...mapState('exports', {'exportsFields': 'getInfoData', 'resultsData': 'postInfoData'}),
      schema () {
        if (!this.exportsFields) {
          return {}
        }

        return {
          fields: {
            type: 'group',
            label: 'Tennañ',
            col: 12,
            class: 'title br-8 elevation-4 mx-2 pa-2 lighten-3',
            schema: {
              fields: {
                type: 'autocomplete',
                multiple: true,
                chips: true,
                clearable: true,
                'deletable-chips': true,
                label: '',
                col: 12,
                items: Object.keys(this.exportsFields)
              },
            },
          },
          operations: {
            type: 'group',
            label: "Lec'h ma",
            col: 12,
            class: 'title br-8 elevation-4 mx-2 pa-2 lighten-3',
            schema: this.operationSchema()
          },
          orders: {
            type: 'group',
            label: "Urzhiañ dre",
            col: 12,
            class: 'title br-8 elevation-4 mx-2 pa-2 lighten-3',
            schema: this.orderSchema()
          },
        }
      },
    },
    mounted () {
      this.$store.dispatch('users/getCurrentUser')
      this.$store.dispatch('exports/getExportFields', 'meurgorf')
    },
    methods: {
      newOperationModel (index) {
        return {
          [`field_${index}`]: '',
          [`operator_${index}`]: '',
          [`value_${index}`]: '',
        }
      },
      operationSchema () {
        let schema = {}
        this.operations.forEach((index) => {
          schema = {
            ...schema,
            [`field_${index}`]: {
              type: 'select',
              label: 'champs',
              col: 4,
              items: this.model.fields.fields,
              noDataText: "Ajouter un champ",
            },
            [`operator_${index}`]: {
              type: 'select',
              label: '',
              col: 2,
              items: ['=', 'contient', 'commence par', 'finit par', '>', '<'],
            },
            [`value_${index}`]: {
              type: 'text',
              label: '',
              col: 4,
            },
            [`delete_${index}`]: { type: 'btn', label:'x', dark: true, color: 'blue lighten-2', class:'mx-1', drop:true },
          }
        })

        return {
          ...schema,
          [`add`]: { type: 'btn', label:'+', col: 6, dark: true, color: 'blue lighten-2', class:'mb-2', },
        }
      },
      newOrderModel (index) {
        return {
          [`field_${index}`]: '',
          [`order_${index}`]: '',
        }
      },
      orderSchema () {
        let schema = {}
        this.orders.forEach((index) => {
          schema = {
            ...schema,
            [`field_${index}`]: {
              type: 'select',
              label: '',
              col: 4,
              items: this.model.fields.fields,
              noDataText: "Ajouter un champ",
            },
            [`order_${index}`]: {
              type: 'select',
              label: '',
              col: 4,
              items: ['Asc', 'Desc'],
            },
            [`delete_${index}`]: { type: 'btn', label:'x', dark: true, color: 'blue lighten-2', class:'mx-1', drop:true },
          }
        })

        return {
          ...schema,
          [`add`]: { type: 'btn', label:'+', col: 6, dark: true, color: 'blue lighten-2', class:'mb-2', },
        }
      },
      addIndex(arr) {
        let index = arr[arr.length - 1] + 1
        if (!index) {
          index = 0
        }
        arr.push(index)

        return index
      },
      log (val) {
        let { id, key } = val

        if (id == "exports-operations") {
          if (key == 'add') {
            this.$nextTick(() => {
              const index = this.addIndex(this.operations)
              this.model.operations = Object.assign({}, this.model.operations, this.newOperationModel(index))
            })
          }
          if (key.startsWith('delete')) {
            this.$nextTick(() => {
              const index = parseInt(key.substring(7))
              this.operations.splice(this.operations.indexOf(index), 1)
              this.$delete(this.model.operations, `field_${index}`)
              this.$delete(this.model.operations, `operator_${index}`)
              this.$delete(this.model.operations, `value_${index}`)
              this.$delete(this.model.operations, `delete_${index}`)
            })
          }
        }
        if (id == 'exports-orders') {
          if (key == 'add') {
            this.$nextTick(() => {
              const index = this.addIndex(this.orders)
              this.model.orders = Object.assign({}, this.model.orders, this.newOrderModel(index))
            })
          }
          if (key.startsWith('delete')) {
            this.$nextTick(() => {
              const index = parseInt(key.substring(7))
              this.orders.splice(this.orders.indexOf(index), 1)
              this.$delete(this.model.orders, `field_${index}`)
              this.$delete(this.model.orders, `order_${index}`)
              this.$delete(this.model.orders, `delete_${index}`)
            })
          }
        }
      },
      as_true_name (obj) {
        Object.keys(obj).forEach(item => {
          if (item.startsWith('field')) {
            obj[item] = this.exportsFields[obj[item]]
          }
        })
      },
      export_data () {
        let data = JSON.parse(JSON.stringify(this.model))
        data['fields']['fields'] = data['fields']['fields'].map(item => this.exportsFields[item])
        this.as_true_name(data['operations'])
        this.as_true_name(data['orders'])
        console.log(data)
        this.$store.dispatch('exports/getExportData', { app_type: "meurgorf", data })
      },
    },
  }
</script>
