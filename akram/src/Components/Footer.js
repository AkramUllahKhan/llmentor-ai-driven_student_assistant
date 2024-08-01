import React from 'react'

export default function Footer() {
    return (
        <div className='mt-2'>
            <footer className="bg-body-tertiary text-center" >

                <div
                    className="text-center p-3 text-light"
                    style={{ backgroundColor: "#C16A3F" }}
                >
                    © 2024 Copyright:
                    <a className="text-reset fw-bold ms-2" href="#">
                        UET Chat Bot
                    </a>
                </div>
            </footer>
        </div>
    )
}
