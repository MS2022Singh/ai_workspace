import argparse
from app import CoreApplication

def main():
    parser = argparse.ArgumentParser(description='AI Workspace Core CLI')
    parser.add_argument('--task_id', required=True, help='Unique Task ID')
    parser.add_argument('--title', required=True, help='Task Title')
    parser.add_argument('--domain', required=True, help='Expert Domain (frontend, backend, qa, pm)')
    
    args = parser.parse_args()
    app = CoreApplication()
    result = app.run_workflow(args.task_id, args.title, args.domain)
    print(f'Workflow Executed Successfully: {result}')

if __name__ == '__main__':
    main()
