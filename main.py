import cond_updater
import xlsx_import


if __name__ == '__main__':
    wb = xlsx_import.get_xlsx_data()
    data = xlsx_import.make_data_dict(wb)
    # print(len(data))
    cond_updater.cond_update(data)
