using UnityEngine;

public class CameraMovement : MonoBehaviour
{
    private Vector3 touchStart;
    private float zoomSpeed = 0.1f;
    private Camera mainCamera;
    private void Start()
    {
        mainCamera = Camera.main;
    }
    private void FixedUpdate()
    {

    }
    private void Update()
    {
        if (Input.touchCount > 0)
        {
            Touch touch = Input.GetTouch(0);
            if (touch.phase == TouchPhase.Began)
            {
                touchStart = mainCamera.ScreenToWorldPoint(touch.position);
            }
            else if (touch.phase == TouchPhase.Moved)
            {
                Vector3 direction = touchStart - mainCamera.ScreenToWorldPoint(touch.position);
                mainCamera.transform.position += new Vector3(direction.x, 0f, direction.z);
            }
        }
        Debug.Log("Active");
        if (Input.GetMouseButtonDown(0))
        {
            touchStart = mainCamera.ScreenToWorldPoint(Input.mousePosition);
        }
        else if (Input.GetMouseButton(0))
        {
            Vector3 direction = touchStart - mainCamera.ScreenToWorldPoint(Input.mousePosition);
            mainCamera.transform.position += direction;
        }

        float scroll = Input.GetAxis("Mouse ScrollWheel");
        mainCamera.orthographicSize -= scroll * zoomSpeed;
        mainCamera.orthographicSize = Mathf.Clamp(mainCamera.orthographicSize, 1f, 10f);
    }
}