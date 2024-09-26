import json
import constants as const
from training_record import TrainingRecord, TrainingState
import boto3
from telebot import types


def get_next_training(user_name):
    next_training = find_next_training()
    if next_training:
        return True, const.NEXT_TRAINING_MESSAGE.format(user_name) + format_training_record(next_training)
    else:
        return False, const.NO_PENDING_TRAININGS_MESSAGE.format(user_name)


def get_trainings_by_state(state: TrainingState):
    result = []
    for training in read_trainings():
        if training["state"] == state.name:
            result.append(training)
    return result


def find_next_training():
    pending_trainings = get_trainings_by_state(TrainingState.pending)
    next_training = pending_trainings[0] if pending_trainings else None
    for training in pending_trainings:
        if training["creation_date"] < next_training["creation_date"]:
            next_training = training
    return next_training


def add_new_training(training_message: types.Message):
    training_record = TrainingRecord(training_message.text, creation_date=training_message.date)
    trainings = read_trainings()
    trainings.append(training_record.to_dict())
    write_trainings(trainings)


def complete_training(training_message: types.Message):
    trainings = read_trainings()
    next_training = find_next_training()
    for training in trainings:
        if training["creation_date"] == next_training["creation_date"]:
            training["state"] = TrainingState.completed.name

    write_trainings(trainings)


def format_training_record(training_record):
    result = "\n\n"
    if 'name' in training_record:
        result += f"Name: {training_record['name']}\n\n"
    result += training_record['description']
    return result


def read_trainings():
    with open('/function/storage/mnt/trainings.json', 'r') as file:
        trainings = json.load(file).get("trainings")
        return trainings


def write_trainings(trainings):
    result = {"trainings": trainings}
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net'
    )
    s3.put_object(Bucket='lorenzo-storage', Key='trainings.json', Body=json.dumps(result), StorageClass='STANDARD')
