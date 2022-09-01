import { formatDate } from '@/utils/dateFormat.js'

export const wuba_dateformat = function (time) {
  var date = new Date(time)
  return formatDate(date, 'yyyy-MM-dd hh:mm:ss')
}
