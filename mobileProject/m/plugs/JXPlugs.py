class page:
    #总页码
    __count = 0
    #每页最大数
    __every_page_count = 10


    current_start_page = 0
    current_page = 0
    current_end_page = 0


    def __init__(self, count):
        self.__count = count


    def comput(self,current_page):
        if current_page > self.__count:
            return
        if current_page < 1:
            return

        current_start_page = 1
        current_end_page = 1

        if self.__count < self.__every_page_count:
            current_start_page = 1
            current_end_page = self.__count
        else:
            if current_page < 7:
                current_start_page = 1
                current_end_page = 10
            else:
                current_end_page = current_page + 3
                if current_end_page > self.__count:
                    current_end_page = self.__count
                current_start_page = current_end_page - 9
        self.current_start_page = current_start_page
        self.current_end_page = current_end_page + 1
        self.current_page = current_page

        return list(range(self.current_start_page, self.current_end_page))