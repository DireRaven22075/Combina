using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
[RequireComponent(typeof(Rigidbody))]
public class PlayerController : MonoBehaviour
{
    //변수 선언부
    #region variable
    private Rigidbody rigid;
    private Camera camera;
    private float yRotation = 0;
    #endregion

    //함수 선언부
    #region Method
    void Move()
    {
        float horizontal = Input.GetAxisRaw("Horizontal"); // 수평 이동 입력 값
        float vertical = Input.GetAxisRaw("Vertical");   // 수직 이동 입력 값

        // 입력에 따라 이동 방향 벡터 계산
        Vector3 moveVec = transform.forward * vertical + transform.right * horizontal;

        // 이동 벡터를 정규화하여 이동 속도와 시간 간격을 곱한 후 현재 위치에 더함
        transform.position += moveVec.normalized * 5 * Time.deltaTime;
    }
    #endregion

    //유니티 내장 함수
    #region Unity Method
    private void Start()
    {
        rigid = GetComponent<Rigidbody>();
    }
    private void Update()
    {
        
    }
    #endregion
}
