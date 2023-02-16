import mlflow

def main():

    with mlflow.start_run() as run:
        mlflow.run('.',"get_data", env_manager='local')
        mlflow.run('.',"base_model_creation", env_manager='local')
        
if __name__ == '__main__':
    main()