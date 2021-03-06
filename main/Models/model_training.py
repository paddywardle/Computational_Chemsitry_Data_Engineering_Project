from MySQL_Database.CreateDB import CreateDB
from DataloaderCreator import DataloaderCreator
from ModelTrainEval import ModelTrainEval
from main.config import configuration_dict

if __name__ == "__main__":

    user = configuration_dict['user']
    password = configuration_dict['password']
    db_name = configuration_dict['db_name']

    # query for image data
    img_query = "SELECT image FROM images"

    # query for labels
    labels_query = "SELECT HBondDonorCount FROM properties"

    # database object
    db = CreateDB(user, password)

    images = db.fetch_query(db_name, img_query)

    labels = db.fetch_query(db_name, labels_query)

    # dataloader object to create training and evaluation datasets
    dataloader = DataloaderCreator(images, labels)

    train_loader, test_loader = dataloader.dataloader_creator(batch_size=4, train_size=0.9)

    # ModelTrainEval object to train the model
    model_trainer = ModelTrainEval()

    training_losses = model_trainer.train_net(num_epochs=10, train_loader=train_loader)

    testing_loss = model_trainer.eval(test_loader=test_loader)