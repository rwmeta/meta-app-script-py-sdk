# coding=utf-8

from metaappscriptsdk import MetaApp

META = MetaApp()
log = META.log

my_global_variable = "FOO"

# Установка таской для отладки кода
META.worker.debug_tasks = [{
    "data": {
        "company_id": 1,
        "campaign_id": 7
    }
}]


def get_companies():
    return [1, 2, 3]


def get_campaigns(company_id):
    return [2, 3, 4, 5]


def process_campaign(company_id_, campaign_id_):
    log.info("Обрабатываем кампанию")


@META.worker.single_task
def main(task):
    data_ = task['data']
    company_id = data_.get('company_id', None)
    campaign_id = data_.get('campaign_id', None)

    log.set_entity('company_id', company_id)
    log.set_entity('campaign_id', campaign_id)

    if not company_id:
        log.info("Ставим таски на агентства")
        for comp_id in get_companies():
            META.starter.build_submit(META.service_id, {"company_id": comp_id})
    elif not campaign_id:
        log.info("Ставим таски на кампании")
        for camp_id in get_campaigns(company_id):
            META.starter.build_submit(META.service_id, {"company_id": company_id, 'campaign_id': camp_id})
    else:
        process_campaign(company_id, campaign_id)
