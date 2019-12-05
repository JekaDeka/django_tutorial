<template>
  <v-card>
    <v-card-title>
      <v-spacer />
      <v-dialog v-model="dialog" max-width="680px">
        <template v-slot:activator="{ on }">
          <v-btn
            color="primary"
            dark
            class="mb-2"
            v-on="on"
          >Новая запись</v-btn>
        </template>
        <v-card>
          <v-card-title>
            <span class="headline">{{ formTitle }}</span>
          </v-card-title>

          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12" sm="6">
                  <v-text-field v-model="editedItem.title" label="Название" />
                </v-col>
                <v-col cols="12" sm="6">
                  <v-menu ref="menu" v-model="menu">
                    <template v-slot:activator="{ on }">
                      <v-text-field
                        v-model="editedItem.published_date"
                        label="Дата публикации"
                        persistent-hint
                        prepend-icon="mdi-calendar"
                        @blur="date = parseDate(editedItem.published_date)"
                        v-on="on"
                      />
                    </template>
                    <v-date-picker
                      v-model="date"
                      no-title
                      @input="menu = false"
                    />
                  </v-menu>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field v-model="editedItem.author" label="Автор" />
                </v-col>
                <v-col cols="12">
                  <v-textarea v-model="editedItem.text" label="Текст" />
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>

          <v-card-actions>
            <v-spacer />
            <v-btn color="error" text @click="close">Отмена</v-btn>
            <v-btn color="primary" @click="save">Сохранить</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-card-title>
    <v-data-table :headers="headers" :items="blogposts" :loading="loading">
      <template v-slot:item.action="{ item }">
        <v-icon small class="mr-2" @click="editItem(item)">
          mdi-pencil
        </v-icon>
        <v-icon small @click="deleteItem(item)">
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
import BlogService from '@/api/blog.service.js'
import { formatDate, parseDate } from '@/utils/date'
export default {
  data() {
    return {
      blogposts: [],
      menu: false,
      dialog: false,
      loading: true,
      date: new Date().toISOString().substr(0, 10),
      headers: [
        { text: 'id', value: 'id' },
        {
          text: 'Название',
          align: 'left',
          value: 'title'
        },
        { text: 'Дата публикации', value: 'published_date' },
        { text: 'Автор', value: 'author' },
        { text: 'Текст', value: 'preview_text' },
        { text: 'Действия', sortable: false, value: 'action' }
      ],
      editedIndex: -1,
      editedItem: {
        id: null,
        published_date: null,
        author: '',
        preview_text: '',
        text: ''
      },
      defaultItem: {
        id: null,
        published_date: null,
        author: '',
        preview_text: '',
        text: ''
      }
    }
  },
  computed: {
    formTitle() {
      return this.editedIndex === -1 ? 'Новая запись' : 'Редактировать запись'
    }
  },
  watch: {
    dialog(val) {
      val || this.close()
    },
    date(val) {
      this.editedItem.published_date = this.formatDate(this.date)
    }
  },
  mounted() {
    this.getDataFromApi()
  },
  methods: {
    getDataFromApi() {
      this.loading = true
      BlogService.getPosts()
        .then(response => {
          this.blogposts = response.data
        })
        .catch(error => {
          console.log(error)
        })
        .finally(() => (this.loading = false))
    },
    editItem(item) {
      this.editedIndex = this.blogposts.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },
    deleteItem(item) {
      const index = this.blogposts.indexOf(item)
      this.editedItem = Object.assign({}, item)
      if (confirm('Вы точно хотите удалить запись?')) {
        this.loading = true
        BlogService.deletePost(this.editedItem.id).then(() => {
          this.loading = false
          this.blogposts.splice(index, 1)
          this.$awn.success('Запись успешно удалена')
        })
      }
    },
    close() {
      this.dialog = false
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      }, 300)
    },
    save() {
      this.loading = true
      BlogService.savePost(this.editedItem)
        .then(response => {
          this.$awn.success('Запись успешно сохранена')
          if (this.editedIndex > -1) {
            Object.assign(this.blogposts[this.editedIndex], this.editedItem)
          } else {
            this.blogposts.push(this.editedItem)
          }
          this.close()
        })
        .catch(error => {
          console.log(error)
        })
    },
    formatDate: formatDate,
    parseDate: parseDate
  }
}
</script>

<style lang="css" scoped></style>
