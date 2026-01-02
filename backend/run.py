import uvicorn
import sys
import os

def main():
    try:
        # Añade el directorio actual al path
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        print("Starting Cutting 2D Optimizer API...")
        print("Press Ctrl+C to stop")
        
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
